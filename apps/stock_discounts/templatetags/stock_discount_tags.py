from django import template

from stock_discounts.models import Product
#
register = template.Library()
#

@register.assignment_tag()
def get_discount_stock():
    qs = Product.active.filter(type_category=2)[:5]
    return qs


