# -*- coding: utf-8 -*-

import hashlib
import os.path

from django.http import HttpResponse
from django.utils import simplejson
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage

class choices_to_dict(tuple):
    '''
    Creates a choices data type like what django needs for models.
    STATUS_CHOICES = django_choices(Draft=1, Public=2, Closed=3)
    STATUS = STATUS_CHOICES.to_dict()
    '''
    def __new__(self, *args, **kwargs):
        self.choices = []
        if kwargs:
            for val in kwargs.values():
                for key in kwargs.keys():
                    if kwargs[key] == val:
                        self.choices.append((val, key))
        return tuple.__new__(self, self.choices or args)

    def to_dict(self):
        '''
        Automatically converts the choices to a dictionary. Useful for type lookups.
        '''
        d = {}
        for choice in self:
            d[choice[1].lower()] = choice[0]
        return d

class JsonResponse(HttpResponse):
    def __init__(self, data):
        HttpResponse.__init__(self,
            content = simplejson.dumps(data, ensure_ascii=False),
            mimetype = 'application/json'
        )


def md5_for_file(chunks):
    md5 = hashlib.md5()
    for data in chunks:
        md5.update(data)
    return md5.hexdigest()


def simple_upload_to(field_name, path='photos'):
    def upload_to(instance, filename):
        name = md5_for_file(getattr(instance, field_name).chunks())
        dot_pos = filename.rfind('.')
        ext = filename[dot_pos:][:10].lower() if dot_pos > -1 else '.unknown'
        name += ext
        return os.path.join(path, name[:2], name)
    return upload_to


def html_escape(text):
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }
    return "".join(html_escape_table.get(c, c) for c in text)


def cached_property(f):
    """A property which value is computed only once and then stored with
    the instance for quick repeated retrieval.
    """
    def _closure(self):
        cache_key = '_cache__%s' % f.__name__
        value = getattr(self, cache_key, None)
        if value == None:
            value = f(self)
            setattr(self, cache_key, value)
        return value
    return property(_closure)


def paginate(object_list, per_page=10, request=None, param_name='page', page=None, **kwargs):
    paginator = Paginator(object_list, per_page, **kwargs)
    if not page:
        try:
            page = int(request.GET.get(param_name, 1))
        except ValueError:
            page = 1
    try:
        page_obj = paginator.page(page)
    except InvalidPage:
        page_obj = paginator.page(1)
    return paginator, page_obj, page


def render_to(template_path, allow_ajax=False):
    '''
    Decorate the django view.
 
    Wrap view that return dict of variables, that should be used for
    rendering the template.
    Dict returned from view could contain special keys:
    * MIME_TYPE: mimetype of response
    * TEMPLATE: template that should be used instead one that was
                specified in decorator argument
    '''
 
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            output = func(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            kwargs = {'context_instance': RequestContext(request)}
 
            if allow_ajax and request.is_ajax():
                return HttpResponse(simplejson.dumps(output, ensure_ascii=False), 'application/json')
 
            if 'MIME_TYPE' in output:
                kwargs['mimetype'] = output.pop('MIME_TYPE')
 
            template = template_path
            if 'TEMPLATE' in output:
                template = output.pop('TEMPLATE')
            return render_to_response(template, output, **kwargs)
        return wrapper
    return decorator

