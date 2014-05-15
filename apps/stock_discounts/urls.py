# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

from .views import ProductDetail, StockDiscountList

urlpatterns = patterns('',
    url(r'^$', StockDiscountList.as_view(), name='stock_discount_index'),

    url(r'^type=(?P<type>[-\d]+)/$', StockDiscountList.as_view(), name='stock_discount_sub_list'),
    url(r'^(?P<slug>[-\w]+)/$', ProductDetail.as_view(), name='stock_discount_detail'),
    # url(r'^(?P<pk>[-\d]+)/$', ProductDetail.as_view(), name='stock_discount_detail'),


    # (r'^(?P<year>\d{4})/$', 'archive_year', link_info_dict, 'coltrane_link_archive_year'),
    #
    # (r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 'archive_month', link_info_dict, 'coltrane_link_archive_month'),
    #
    # (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', 'archive_day', link_info_dict, 'coltrane_link_archive_day'),
    #
    # (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'object_detail', link_info_dict, 'coltrane_link_detail'),

)