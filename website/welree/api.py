#from tastypie.fields import RelatedField
from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields.related import RelatedField
from django.forms import ModelForm
from django.forms.models import model_to_dict
from tastypie import fields
from tastypie.api import Api
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.exceptions import Unauthorized
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie.validation import CleanedDataFormValidation, FormValidation
import tastypie

from welree import models, forms

v1 = Api('v1')


# https://github.com/django-tastypie/django-tastypie/issues/152
class ModelFormValidation(FormValidation):
    def form_args(self, bundle):
        '''
        Use the model data to generate the form arguments to be used for
        validation.  In the case of fields that had to be hydrated (such as
        FK relationships), be sure to use the hydrated value (comes from 
        model_to_dict()) rather than the value in bundle.data, since the latter
        would likely not validate as the form won't expect a URI.
        '''
        data = bundle.data

        # Ensure we get a bound Form, regardless of the state of the bundle.
        if data is None:
            data = {}

        kwargs = {'data': {}}
        if hasattr(bundle.obj, 'pk'):
            if issubclass(self.form_class, ModelForm):
                kwargs['instance'] = bundle.obj

            kwargs['data'] = model_to_dict(bundle.obj)
            # iterate over the fields in the object and find those that are
            # related fields - FK, M2M, O2M, etc.  In those cases, we need
            # to *not* use the data in the bundle, since it is a URI to a
            # resource.  Instead, use the output of model_to_dict for 
            # validation, since that is already properly hydrated.
            for field in bundle.obj._meta.fields:
                if field.name in bundle.data: 
                    if not isinstance(field, RelatedField):
                        kwargs['data'][field.name]=bundle.data[field.name]
        else:
            kwargs['data'].update(data)
        return kwargs

    def is_valid(self, bundle, request=None):
        """
        Checks ``bundle.data``to ensure it is valid & replaces it with the
        cleaned results.
        If the form is valid, an empty list (all valid) will be returned. If
        not, a list of errors will be returned.
        """
        form = self.form_class(**self.form_args(bundle))

        if form.is_valid():
            # We're different here & relying on having a reference to the same
            # bundle the rest of the process is using.
            bundle.data = form.cleaned_data
            return {}

        # The data is invalid. Let's collect all the error messages & return
        # them.
        return form.errors

class OwnerObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(owner=bundle.request.user.id)

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return bundle.obj.owner.id == bundle.request.user.id

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.owner.id == bundle.request.user.id

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.owner.id == bundle.request.user.id:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.owner.id == bundle.request.user.id

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

class MultipartResource(object):
    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(MultipartResource, self).deserialize(request, data, format)

class OwnerModelResource(MultipartResource, ModelResource):
    def hydrate(self, bundle, request=None):
        bundle.obj.owner = get_user_model().objects.filter(pk=bundle.request.user.id).first()
        return bundle

class JewelryCollectionResource(OwnerModelResource):
    class Meta:
        queryset = models.JewelryCollection.objects.all()
        fields = []
        allowed_methods = ['get', 'post']
        resource_name = 'collection'
        authorization = OwnerObjectsOnlyAuthorization()
        @property
        def validation(self):
            return ModelFormValidation(form_class=forms.CollectionForm, resource=JewelryCollectionResource)

class JewelryItemResource(OwnerModelResource):
    primary_photo = fields.FileField(attribute="primary_photo")
    collection = tastypie.fields.ForeignKey(JewelryCollectionResource, 'collection')

    class Meta:
        always_return_data = True
        queryset = models.JewelryItem.curated.all()
        fields = []
        allowed_methods = ['get', 'post']
        resource_name = 'jewelry'
        authorization = OwnerObjectsOnlyAuthorization()
        @property
        def validation(self):
            return ModelFormValidation(form_class=forms.JewelryItemForm, resource=JewelryItemResource)

    def hydrate_collection(self, bundle):
        if 'collection' in bundle.data:
            bundle.data['collection'] = '/api/v1/collection/{}/'.format(bundle.data['collection'])
        return bundle

class UserResource(ModelResource):
    class Meta:
        queryset = get_user_model().objects.all()
        fields = ['first_name', 'last_name', 'email']
        allowed_methods = ['get', 'post']
        resource_name = 'user'
        authorization = DjangoAuthorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
            url(r'^(?P<resource_name>%s)/signup%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('signup'), name='api_signup'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                    }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
                }, HttpUnauthorized )

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)

    def signup(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        signup_form = forms.SignupForm(data)
        if signup_form.is_valid():
            user = models.CustomUser.signup(signup_form)
            response = {
                    'success': True,
                    'user_id': user.id,
            }
        else:
            response = {
                    'success': False,
                    'reason': signup_form.errors,
            }
        return self.create_response(request, response)

v1.register(UserResource())
v1.register(JewelryItemResource())
v1.register(JewelryCollectionResource())
