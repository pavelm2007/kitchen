# -*- coding: utf-8 -*-
from django import forms
from common.widget import AdminImageWidget
from flatcontent.models import FlatContent
from cked.widgets import CKEditorWidget
from .models import Photo


class FlatContentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget)

    class Meta:
        model = FlatContent


class ImageForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image','main_image', 'title', )
        widgets = {
            'image': AdminImageWidget,
        }
