from django import template

from products.models import Category

register = template.Library()


@register.assignment_tag()
def get_product_category():
    qs = Category.objects.all()
    return qs

