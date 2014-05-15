from django.contrib import admin
from django.db import models
from .models import FlatPage, Block
from django.utils.translation import ugettext_lazy as _
from .forms import FlatpageForm

from cked.widgets import CKEditorWidget

class FlatpageBlockAdmin(admin.StackedInline):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }
    model = Block
    extra = 1

class FlatPageAdmin(admin.ModelAdmin):
    form = FlatpageForm
    # fieldsets = (
    #     (None, {'fields': ('url', 'title', 'content', 'sites')}),
    #     # (None, {'fields': ('url', 'title','image', 'content', 'sites')}),
    #     (_('Advanced options'), {'classes': ('collapse',), 'fields': ('enable_comments', 'registration_required', 'template_name')}),
    #     # (_('SEO'), {'classes': ('collapse',), 'fields': ('head_title', 'meta_keywords', 'meta_description')}),
    # )
    list_display = ('url', 'title')
    list_filter = ('sites', 'enable_comments', 'registration_required')
    search_fields = ('url', 'title')
    inlines = [FlatpageBlockAdmin,]

admin.site.register(FlatPage, FlatPageAdmin)

