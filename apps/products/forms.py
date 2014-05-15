# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext, ugettext_lazy as _

from cked.widgets import CKEditorWidget

from .models import Product, Category


class ProductAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget, required=False)

    class Meta:
        model = Product
