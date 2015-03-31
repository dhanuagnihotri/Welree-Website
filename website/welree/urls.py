from django.conf.urls import *
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy

from welree.api import v1

admin.autodiscover()

app_urls = (
    url(r'^%s/'%name, 'welree.views.%s'%name.replace('/', '_'), name=name.replace('/', '_')) for name in (
        'login',
        'logout',
        'signup',
        'account',
        'events',
        'designer/upload',
        'consumer/upload',
    )
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^password_reset$', 'welree.views.password_reset', kwargs={'template_name': 'password_reset_form.jinja', 'post_reset_redirect': reverse_lazy('password_reset_done'), 'email_template_name': 'password_reset_email.html'}, name="password_reset"),
    url(r'^password_reset/done$', 'welree.views.password_reset_done', name="password_reset_done"),
    url(r'^reset(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', kwargs={'template_name': 'password_reset_confirm.html'}),
    url(r'^reset/done$', 'django.contrib.auth.views.password_reset_complete', kwargs={'template_name': 'password_reset_complete.html'}, name='password_reset_complete'),

    url(r'^$', 'welree.views.home', name="home"),
    url(r'^email/confirm/(?P<token>[\w-]{36})/$', 'welree.views.email_confirm', name="email_confirm"),

    url(r'', include('social.apps.django_app.urls', namespace='social')),


    url(r'^item/(?P<coll_pk>[\d]+)-(?P<item_pk>[\d]+)/', 'welree.views.item', name="item"),

    url(r'^api/', include(v1.urls, namespace='tastypie')),
    url(r'^api/docs/',
      include('tastypie_swagger.urls', namespace='tastypie_swagger'),
      kwargs={'tastypie_api_module': 'welree.api.v1', 'namespace':'tastypie_swagger'}
    ),

    *app_urls
)
