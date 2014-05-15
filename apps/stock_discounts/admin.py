# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from cked.widgets import CKEditorWidget

from common.admin import PhotoStakedAdmin
from common.widget import AdminImageWidget

from .models import Product


class StockDiscountAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
        models.ImageField: {'widget': AdminImageWidget()},
    }
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('is_active',)
    list_display = ( 'admin_thumbnail', 'title',)
    list_display_links = ('admin_thumbnail', 'title',)
    fieldsets = (
        (None, {
            'fields': ('type_category',('position','is_active',),('title', 'slug'), ('image',), 'body',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('head_title', 'meta_description', 'meta_keywords')
        }),
    )
    inlines = [PhotoStakedAdmin, ]


admin.site.register(Product, StockDiscountAdmin)