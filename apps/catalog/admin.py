# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from cked.widgets import CKEditorWidget
from mptt.admin import MPTTModelAdmin
from feincms.admin import tree_editor

from .models import Category, Works, Facade, MillingFacade, Finding, Tabletop, Ldsp, PhotoPrinting, Project
from .forms import *
from common.admin import PhotoStakedAdmin
from common.widget import AdminImageWidget


# class CategoryAdmin(admin.ModelAdmin):
class CategoryMPTTModelAdmin(tree_editor.TreeEditor):
    save_on_top = True
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
        models.ImageField: {'widget': AdminImageWidget()},
    }
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('is_active',)
    list_display = ('name', 'position', 'view',)
    list_display_links = ('name',)
    list_editable = ('position',)
    fieldsets = (
        (None, {
            'fields': (
            ('parent', 'content_type', 'view', 'page'), ('position', 'is_active',), ('name', 'slug'), 'image',
            'description', )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('head_title', 'meta_description', 'meta_keywords')
        }),
    )


admin.site.register(Category, CategoryMPTTModelAdmin)


class BaseItemAdmin(admin.ModelAdmin):
    save_on_top = True
    # form = WorkAdminForm
    list_filter = ('is_active', )
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('admin_thumbnail', 'position', 'name', 'category', )
    list_display_links = ('admin_thumbnail', 'name', )
    list_editable = ('position','category', )
    fieldsets = (
        (None, {
            'fields': (
            'category',
            ('position', 'is_active',), ('name', 'slug'), 'price', ('image', 'excerpt'), 'body', 'featured',
            'tags',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('head_title', 'meta_description', 'meta_keywords')
        }),
    )
    inlines = [PhotoStakedAdmin, ]


class WorksAdmin(BaseItemAdmin):
    form = WorkAdminForm


admin.site.register(Works, WorksAdmin)


class ProjectAdmin(BaseItemAdmin):
    form = ProjectAdminForm


admin.site.register(Project, ProjectAdmin)


class FacadeAdmin(BaseItemAdmin):
    form = FacadeAdminForm


admin.site.register(Facade, FacadeAdmin)


class MillingFacadeAdmin(BaseItemAdmin):
    form = MillingFacadeAdminForm


admin.site.register(MillingFacade, MillingFacadeAdmin)


class FindingAdmin(BaseItemAdmin):
    form = FindingAdminForm


admin.site.register(Finding, FindingAdmin)


class TabletopAdmin(BaseItemAdmin):
    form = TabletopAdminForm


admin.site.register(Tabletop, TabletopAdmin)


class LdspAdmin(BaseItemAdmin):
    form = LdspAdminForm


admin.site.register(Ldsp, LdspAdmin)


class PhotoPrintingAdmin(BaseItemAdmin):
    form = PhotoPrintingAdminForm


admin.site.register(PhotoPrinting, PhotoPrintingAdmin)
