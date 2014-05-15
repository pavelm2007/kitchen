from django import template
from django.db.models.loading import get_model

from catalog.models import Category, Works, Project

register = template.Library()


@register.assignment_tag()
def get_root_category():
    qs = Category.tree.root_nodes()
    return qs


@register.assignment_tag()
def get_works_category():
    works = get_model('catalog', 'works')
    filter_list = {
        'parent__isnull': False,
        'content_type_model': 'works',
    }
    qs = Category.objects.filter(**filter_list)
    return qs


@register.assignment_tag()
def get_future_works():
    # works = get_model('catalog', 'works')
    # filter_list = {
    #     'category__slug': 'proekty',
    # }
    # qs = works.objects.filter(**filter_list).order_by('?')[:35]
    qs = Project.objects.all().order_by('?')[:35]
    return qs

    # @register.assignment_tag()
    # def get_future_works():
    #     works = get_model('catalog', 'works')
    #     filter_list = {
    #         'category__slug': 'proekty',
    #     }
    #     qs = works.objects.filter(**filter_list).order_by('?')[:35]
    #     return qs