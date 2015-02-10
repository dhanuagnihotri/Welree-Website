from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout, get_user_model
from tastypie.api import Api
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.exceptions import Unauthorized
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
import tastypie

from welree import models

v1 = Api('v1')


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
        print bundle.obj.owner
        return bundle

class JewelryCollectionResource(OwnerModelResource):
    class Meta:
        queryset = models.JewelryCollection.objects.all()
        fields = []
        allowed_methods = ['get', 'post']
        resource_name = 'collection'
        authorization = OwnerObjectsOnlyAuthorization()

class JewelryItemResource(OwnerModelResource):
    collection = tastypie.fields.ForeignKey(JewelryCollectionResource, 'collection')

    class Meta:
        queryset = models.JewelryItem.objects.all()
        fields = []
        allowed_methods = ['get', 'post']
        resource_name = 'jewelry'
        authorization = OwnerObjectsOnlyAuthorization()

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
