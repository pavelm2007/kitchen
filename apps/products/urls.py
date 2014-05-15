# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

from .models import Category, Product
from .views import ProductDetail, CategoryList, CategoryDetail

urlpatterns = patterns('',

    url(r'^(?P<parent_slug>[-\w]+)/(?P<slug>[-\w]+)/$', CategoryList.as_view(), name='product_category_parent'),
    url(r'^(?P<parent_slug>[-\w]+)/(?P<slug>[-\w]+)/(?P<pk>[-\d]+)/$', ProductDetail.as_view(), name='product_detail'),
    # url(r'^(?P<slug>[-\w]+)/$', CategoryDetail.as_view(), name='product_category_list'),
    url(r'^(?P<slug>[-\w]+)/$', CategoryList.as_view(), name='product_category_list'),
    url(r'^$', CategoryList.as_view(), name='product_index'),

    # (r'^(?P<year>\d{4})/$', 'archive_year', link_info_dict, 'coltrane_link_archive_year'),
    #
    # (r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 'archive_month', link_info_dict, 'coltrane_link_archive_month'),
    #
    # (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', 'archive_day', link_info_dict, 'coltrane_link_archive_day'),
    #
    # (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'object_detail', link_info_dict, 'coltrane_link_detail'),

)