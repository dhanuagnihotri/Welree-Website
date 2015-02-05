from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout, get_user_model
from tastypie.api import Api
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from welree import models

v1 = Api('v1')

class JewelryItemResource(ModelResource):
    class Meta:
        queryset = models.JewelryItem.objects.all()
        fields = []
        allowed_methods = ['get', 'post']
        resource_name = 'jewelry'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/upload%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('upload'), name="api_upload"),
        ]

    def upload(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        if not (request.user and request.user.is_authenticated()):
            return self.create_response(request, {'success': False, 'reason': 'loggedout'})

        return self.create_response(request, {'success': True})

class UserResource(ModelResource):
    class Meta:
        queryset = get_user_model().objects.all()
        fields = ['first_name', 'last_name', 'email']
        allowed_methods = ['get', 'post']
        resource_name = 'user'

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
