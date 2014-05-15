# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models.loading import get_model

from .models import Category, Works, Facade, MillingFacade, Finding, Tabletop, Ldsp, PhotoPrinting
from .models import ITEM_CONTENT_TYPES, items_content_types_filters


class CategoryMixin(object):

    model_name = None

    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        categories = Category.active.all()
        context.update(
            {
                'category_list': categories,
            }
        )
        model_name = self.kwargs.get('model_name')
        slug = self.kwargs.get('slug')
        # current_category = None
        if slug and model_name == 'works':
            current_category = categories.get(slug=slug)
        if slug and model_name == 'project':
            current_category = categories.get(slug=slug)
        if model_name in ITEM_CONTENT_TYPES and model_name != 'works' and model_name != 'project':
            current_category = categories.get(content_type_model=model_name)
        if model_name not in ITEM_CONTENT_TYPES:
            current_category = categories.get(slug=model_name)
        if current_category:

            context.update(
                {
                    'current_category': current_category,
                    # 'current_category': categories.get(slug=slug),
                }
            )
        return context



class ItemList(CategoryMixin, ListView):
    template_name = 'catalog/item_list.html'
    model = None


    def get_template_names(self):
        model_name = self.kwargs.get('model_name')
        slug = self.kwargs.get('slug')
        if model_name in ITEM_CONTENT_TYPES:
            self.paginate_by = 10
            return 'catalog/item_list.html'
        else:
            return 'catalog/category_children_list.html'

    def get_queryset(self):
        model_name = self.kwargs.get('model_name')
        slug = self.kwargs.get('slug')
        if model_name in ITEM_CONTENT_TYPES and model_name == 'works' or model_name == 'project':
            self.model = get_model('catalog', model_name)
            if Category.active.get(slug=slug).parent:
                qs = self.model.active.filter(category__slug=slug)
            else:
                qs = Category.active.filter(parent__slug=slug)
            # qs = Works.active.filter(category__slug=slug)
        if model_name in ITEM_CONTENT_TYPES and model_name != 'works' and model_name != 'project':
            self.model = get_model('catalog', model_name)
            qs = self.model.active.all()
        elif model_name not in ITEM_CONTENT_TYPES:
            self.model = Category
            qs = Category.active.filter(parent__slug=self.kwargs.get('model_name'))
        return qs


class ItemDetail(CategoryMixin, DetailView):
    template_name = 'catalog/item_detail.html'

    def get_object(self, queryset=None):
        model = self.kwargs.get('model_name')
        if model in ITEM_CONTENT_TYPES:
            self.model = get_model('catalog', model)

        return super(ItemDetail, self).get_object()
