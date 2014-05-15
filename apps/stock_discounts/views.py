# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from .models import Product


class StockDiscountList(ListView):
    model = Product
    paginator_class = Paginator
    paginate_by = 12
    template_name = 'stock_discounts/product_list.html'

    def get_queryset(self):
        type_cat = self.kwargs.get('type')
        if type_cat:
            return self.model.active.filter(type_category=type_cat)
        return self.model.active.all()

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        type_cat = self.kwargs.get('type')
        if type_cat:
            for key, value in self.model.TYPE_CHOICES:
                if int(key) == int(type_cat):
                    # cat = ({value: reverse('stock_discount_sub_list', kwargs={'type': type_cat})})
                    cat_name = value
                    cat_url = reverse('stock_discount_sub_list', kwargs={'type': type_cat})
        else:
            # cat=({u'Акции/Скидки':reverse('stock_discount_index')})
            cat_name = u'Акции/Скидки'
            cat_url = reverse('stock_discount_index')
        context.update(
            {
                'current_category': cat_name,
                'current_url': cat_url,
            }
        )
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'stock_discounts/product_detail.html'
