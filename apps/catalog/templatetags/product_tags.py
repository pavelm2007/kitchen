from django import template

from catalog.models import Category

register = template.Library()


@register.assignment_tag()
def get_product_category():
    qs = Category.objects.all()
    return qs

@register.assignment_tag()
def get_root_category():
    qs = Category.get_root()
    return qs

