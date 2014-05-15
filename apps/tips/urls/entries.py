from django.conf.urls.defaults import *

from tips.models import Tip
from tips.views import *

entry_info_dict = {
    'queryset': Tip.live.all(),
    'date_field': 'pub_date',
}

urlpatterns = patterns('',
     url(r'^$', TipList.as_view(), name='tips_list'),
     # url(r'^(?P<slug>[-\w]+)/$', TipList.as_view(), name='tip_detail'),
    # (r'^$', 'archive_index', tip_info_dict, 'tips_tip_archive_index'),
    #
    # (r'^(?P<year>\d{4})/$', 'archive_year', tip_info_dict, 'tips_tip_archive_year'),
    #
    # (r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 'archive_month', tip_info_dict, 'tips_tip_archive_month'),
    #
    # (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', 'archive_day', tip_info_dict, 'tips_tip_archive_day'),
    #
    url(r'^(?P<slug>[-\w]+)/$', TipDetail.as_view(),name='tip_detail'),
    # url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', TipDetail.as_view(),name='tip_detail'),
)