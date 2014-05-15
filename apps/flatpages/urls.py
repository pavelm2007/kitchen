from django.conf.urls import patterns
from .views import flatpage

urlpatterns = patterns('',
    (r'^(?P<url>.*)$', 'flatpage'),
)
