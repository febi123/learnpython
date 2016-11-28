"""
Definition of urls for djangocrawler.
"""

from datetime import datetime
from django.conf.urls import url, include
import django.contrib.auth.views

import predictapp.forms
from rest_framework.authtoken import views
# import predictapp.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()
from django.conf.urls import url, include
from predictapp import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'predictlog', views.PredictlogViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'predictgender', views.PredictgenderViewSet, base_name='predictgender')

urlpatterns = [
    # Examples:
    url(r'^$', predictapp.views.home, name='home'),
    url(r'^', include('predictapp.urls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^runmodel', predictapp.views.runmodel, name='runmodel'),
    url(r'^predictasync', predictapp.views.predictasync, name='predictasync'),
    url(r'^contact$', predictapp.views.contact, name='contact'),
    url(r'^about', predictapp.views.about, name='about'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', predictapp.views.obtain_auth_token),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'predictapp/login.html',
            'authentication_form': predictapp.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
