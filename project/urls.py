from django.conf.urls import patterns, include, url, handler403, handler404, handler500
from django.views.generic import TemplateView
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from common.views import Main_Page

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^cked/', include('cked.urls')),

                       url(r'^stock_discounts/', include('stock_discounts.urls')),

                       url(r'^tips/', include('tips.urls.entries')),
                       url(r'^news/', include('coltrane.urls.entries')),
                       url(r'^feedback/', include('feedback.urls')),
                       url(r'^page/', include('flatpages.urls')),
                       url(r'^catalog/', include('catalog.urls', namespace='catalog')),
                       url(r'^$', Main_Page.as_view(), name='index'),

                       # Examples:
                       # url(r'^$', 'project.views.home', name='home'),
                       # url(r'^project/', include('project.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),

)

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT}),
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.STATICFILES_DIRS}),
    )

urlpatterns += patterns('flatpages.views',
                        url(r'^contact/$', 'flatpage', {'url': '/contact/'}, name='contact'),
                        url(r'^questions/$', 'flatpage', {'url': '/questions/'}, name='questions'),
                        # url(r'^contacts/', 'flatpage', {
                        #     'url': '/contacts/'}, name='contacts'),
                        (r'^page/(?P<url>.*)$', 'flatpage'),

)

handler403 = 'common.views.Error403'
handler404 = 'common.views.Error404'
handler500 = 'common.views.Error500'

