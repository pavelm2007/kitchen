# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.contenttypes.generic import ContentType
from django.utils.translation import ugettext, ugettext_lazy as _

from cked.widgets import CKEditorWidget

from common.widget import AdminImageWidget

from .models import Works, Facade, MillingFacade, Finding, Tabletop, Ldsp, PhotoPrinting, Category, Project


class BaseProductAdmin(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget, required=False)
    image = forms.ImageField(widget=AdminImageWidget, required=False)

    class Meta:
        model = Works

    def __init__(self, *args, **kwargs):
        super(BaseProductAdmin, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(
            content_type_model=str(self.Meta.model.__name__.lower()))


class WorkAdminForm(BaseProductAdmin):
    class Meta:
        model = Works


class ProjectAdminForm(BaseProductAdmin):
    class Meta:
        model = Project


class FacadeAdminForm(BaseProductAdmin):
    class Meta:
        model = Facade


class MillingFacadeAdminForm(BaseProductAdmin):
    class Meta:
        model = MillingFacade


class FindingAdminForm(BaseProductAdmin):
    class Meta:
        model = Finding


class TabletopAdminForm(BaseProductAdmin):
    class Meta:
        model = Tabletop


class LdspAdminForm(BaseProductAdmin):
    class Meta:
        model = Ldsp


class PhotoPrintingAdminForm(BaseProductAdmin):
    class Meta:
        model = PhotoPrinting
