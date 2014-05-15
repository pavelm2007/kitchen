from django.contrib import admin
from django.db import models
from coltrane.models import Entry, Block
from django import forms
from cked.widgets import CKEditorWidget
from common.widget import AdminImageWidget


class BlockAdmin(admin.StackedInline):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }
    model = Block
    extra = 1


class EntryAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())
    image = forms.ImageField(widget=AdminImageWidget(), required=False)

    class Meta:
        model = Entry
        fields = ( 'title', 'slug', 'image', 'short_text', 'text', 'pub_date', 'status', )


# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ['title']}
#
#
# admin.site.register(Category, CategoryAdmin)
#

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    form = EntryAdminForm
    inlines = [BlockAdmin]


admin.site.register(Entry, EntryAdmin)


