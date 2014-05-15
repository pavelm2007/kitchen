# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.conf import settings


class Main_Page(TemplateView):
    template_name = 'index.html'


def robots(request):
    from django.http import HttpResponse

    return HttpResponse("User-agent: *\nDisallow: /admin/\nSitemap: http://%s/sitemap.xml" % request.get_host(),
                            mimetype="text/plain")


class Error403(TemplateView):
    template_name = '404.html'


class Error404(TemplateView):
    template_name = '404.html'


class Error500(TemplateView):
    template_name = '500.html'