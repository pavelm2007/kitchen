from django.conf.urls.defaults import *

from coltrane.models import Entry
from coltrane.views import *

entry_info_dict = {
    'queryset': Entry.live.all(),
    'date_field': 'pub_date',
}

urlpatterns = patterns('',
     url(r'^$', EntryList.as_view(), name='entry_list'),
     # url(r'^(?P<slug>[-\w]+)/$', EntryList.as_view(), name='entry_detail'),
    # (r'^$', 'archive_index', entry_info_dict, 'coltrane_entry_archive_index'),
    #
    # (r'^(?P<year>\d{4})/$', 'archive_year', entry_info_dict, 'coltrane_entry_archive_year'),
    #
    # (r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 'archive_month', entry_info_dict, 'coltrane_entry_archive_month'),
    #
    # (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', 'archive_day', entry_info_dict, 'coltrane_entry_archive_day'),
    #
    url(r'^(?P<slug>[-\w]+)/$', EntryDetail.as_view(),name='entry_detail'),
    # url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', EntryDetail.as_view(),name='entry_detail'),
)