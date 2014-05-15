from django.conf.urls import *

from .views import leave_feedback, order_feedback, Sended, Comment
from django.views.generic import TemplateView

urlpatterns = patterns('',
                       url(r'^$', leave_feedback, name='leave_feedback'),
                       url(r'^order$', order_feedback, name='order_feedback'),
                       url(r'^sended/$', Sended.as_view(), name='feedback_sended'),
                       url(r'^comment/$', Comment.as_view(), name='feedback_list'),

)
