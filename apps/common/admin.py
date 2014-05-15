# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.contrib.contenttypes import generic
from django import forms
#from django_markdown.widgets import MarkdownWidget

from flatcontent.models import FlatContent
from flatcontent.admin import FlatContentAdmin
from cked.widgets import CKEditorWidget
from .forms import ImageForm, FlatContentForm
from .models import Photo, Slider
from .widget import AdminImageWidget


class FlatContentAdminCustom(admin.ModelAdmin):
    form = FlatContentForm


admin.site.unregister(FlatContent)
admin.site.register(FlatContent, FlatContentAdminCustom)


class PhotoAdmin(admin.ModelAdmin):
    form = ImageForm
    model = Photo
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}


admin.site.register(Photo, PhotoAdmin)


class PhotoStakedAdmin(generic.GenericTabularInline):
    form = ImageForm
    model = Photo
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}

#    extra = 0



class SliderAdmin(admin.ModelAdmin):
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget},
                           models.TextField: {'widget': CKEditorWidget}}
    list_display = ('is_active', 'position', 'admin_thumbnail', 'title', 'description')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'position',)
    list_display_links = ('title', 'admin_thumbnail',)
    fieldsets = (
        (None, {
            'fields': ('is_active', 'position', 'image', 'title', 'description', )
        }),
        #        ('Seo', {
        #            'classes': ('collapse',),
        #            'fields': ('head_title', 'meta_description', 'meta_keywords')
        #        }),
    )


admin.site.register(Slider, SliderAdmin)