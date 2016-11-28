# from django.conf.urls import patterns, include, url
# from rest_framework.urlpatterns import  format_suffix_patterns
# from predictapp import views
#
# urlpattern = patterns

from django.conf.urls import url
from predictapp import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Predict Gender API')

from predictapp.views import PredictlogViewSet, UserViewSet, api_root, PredictgenderViewSet
from rest_framework import renderers

predictlog_list = PredictlogViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
predictlog_detail = PredictlogViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
predictlog_highlight = PredictlogViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})
predictgender_predict = PredictgenderViewSet.as_view({
    'post': 'create'
})
predictgender_predictname = PredictgenderViewSet.as_view({
    'get': 'retrieve'
})
urlpatterns = [
    # url(r'^predictlog/$', views.PredictlogList.as_view()),
    # url(r'^predictlog/(?P<pk>[0-9]+)/$', views.PredictlogDetail.as_view()),
    # url(r'^users/$', views.UserList.as_view()),
    # url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    # url(r'^$', views.api_root),
    # url(r'^predictlog/(?P<pk>[0-9]+)/highlight/$', views.PredictlogHighlight.as_view()),

    # url(r'^$', views.api_root),
    # url(r'^predictlog/$',
    #     views.PredictlogList.as_view(),
    #     name='predictlog-list'),
    # url(r'^predictlog/(?P<pk>[0-9]+)/$',
    #     views.PredictlogDetail.as_view(),
    #     name='predictlog-detail'),
    # url(r'^predictlog/(?P<pk>[0-9]+)/highlight/$',
    #     views.PredictlogHighlight.as_view(),
    #     name='predictlog-highlight'),
    # url(r'^users/$',
    #     views.PredictlogList.as_view(),
    #     name='user-list'),
    # url(r'^users/(?P<pk>[0-9]+)/$',
    #     views.PredictlogDetail.as_view(),
    #     name='user-detail'),

    url('^schema/$', schema_view),
    url(r'^$', api_root),
    url(r'^predictlog/$', predictlog_list, name='predictlog-list'),
    url(r'^predictlog/(?P<pk>[0-9]+)/$', predictlog_detail, name='predictlog-detail'),
    url(r'^predictlog/(?P<pk>[0-9]+)/highlight/$', predictlog_highlight, name='predictlog-highlight'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
    url(r'^predictgender/$', predictgender_predict, name='predictgender-predict'),
    url(r'^predictgender/(?P<nama>\w{0,250})/(?P<suku>\w{0,250})/$', predictgender_predictname, name='predictgender-predictname'),
    url(r'^predictgender/(?P<nama>\w{0,250})/$', predictgender_predictname, name='predictgender-predictname'),
]


urlpatterns = format_suffix_patterns(urlpatterns)