# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from .models import Category, Product


class CategoryMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        categories = Category.active.all()
        context.update(
            {
                'category_list': categories,
            }
        )
        slug = self.kwargs.get('slug')
        if slug:

            context.update(
                {
                    'current_category': get_object_or_404(Category, slug=slug),
                    # 'current_category': categories.get(slug=slug),
                }
            )
        return context

class CategoryList(CategoryMixin, ListView):
    model = Category
    paginator_class = Paginator
    paginate_by = 12
    template_name = 'products/product_list.html'
    context_object_name = 'nodes'

    def get_template_names(self):
        slug = self.kwargs.get('slug')
        parent_slug = self.kwargs.get('parent_slug')
        if parent_slug:
            return 'products/category_children_list.html'
        if slug:
            return 'products/product_list.html'
        return 'products/product_list_all.html'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        parent_slug = self.kwargs.get('parent_slug')
        if parent_slug and slug:
            return self.model.objects.filter(slug=slug)
        if slug:
            return self.model.objects.filter(slug=slug)

        return self.model.tree.filter(parent=None)


class CategoryDetail(CategoryMixin, DetailView):
    model = Category
    template_name = 'products/category-detail.html'


class ProductDetail(CategoryMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
