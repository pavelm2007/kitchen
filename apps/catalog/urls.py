# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

from catalog.views import ItemList, ItemDetail

urlpatterns = patterns('',
                       url(r'^(?P<model_name>[-\w]+)/$', ItemList.as_view(),
                           name='category_detail'),
                       url(r'^(?P<model_name>[-\w]+)/(?P<slug>[-\w]+)/$', ItemList.as_view(),
                           name='work_category_detail'),
                       url(r'^(?P<model_name>[-\w]+)/item=(?P<pk>[-\d]+)/$', ItemDetail.as_view(),
                           name='item_detail'),
                       url(r'^(?P<model_name>[-\w]+)/(?P<slug>[-\w]+)/item=(?P<pk>[-\d]+)/$', ItemDetail.as_view(),
                           name='work_detail'),
                       # url(r'^$', CategoryList.as_view(), name='index'),
)