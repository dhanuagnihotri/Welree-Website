from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields.related import RelatedField
from tastypie.api import Api
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.exceptions import Unauthorized
#from tastypie.fields import RelatedField
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie.validation import CleanedDataFormValidation, FormValidation
import tastypie

from welree import models, forms

v1 = Api('v1')


# https://github.com/django-tastypie/django-tastypie/issues/152
class ModelFormValidation(FormValidation):
    """
    Override tastypie's standard ``FormValidation`` since this does not care
    about URI to PK conversion for ``ToOneField`` or ``ToManyField``.
    """

    resource = ModelResource

    def __init__(self, **kwargs):
        if not 'resource' in kwargs:
            raise ImproperlyConfigured("You must provide a 'resource' to 'ModelFormValidation' classes.")

        self.resource = kwargs.pop('resource')

        super(ModelFormValidation, self).__init__(**kwargs)


    def _get_pk_from_resource_uri(self, resource_field, resource_uri):
        """ Return the pk of a resource URI """
        base_resource_uri = resource_field.to().get_resource_uri()
        if not resource_uri.startswith(base_resource_uri):
            raise Exception("Couldn't match resource_uri {0} with {1}".format(
                                        resource_uri, base_resource_uri))
        before, after = resource_uri.split(base_resource_uri)
        return after[:-1] if after.endswith('/') else after

    def form_args(self, bundle):
        rsc = self.resource()
        kwargs = super(ModelFormValidation, self).form_args(bundle)

        for name, rel_field in rsc.fields.items():
            data = kwargs['data']
            if not issubclass(rel_field.__class__, RelatedField):
                continue # Not a resource field
            if name in data and data[name] is not None:
                resource_uri = (data[name] if rel_field.full is False
                                            else data[name]['resource_uri'])
                pk = self._get_pk_from_resource_uri(rel_field, resource_uri)
                kwargs['data'][name] = pk

        return kwargs

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


class OwnerModelResource(ModelResource):
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
    collection = tastypie.fields.ForeignKey(JewelryCollectionResource, 'collection')

    class Meta:
        queryset = models.JewelryItem.objects.all()
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

v1.register(UserResource())
v1.register(JewelryItemResource())
v1.register(JewelryCollectionResource())
