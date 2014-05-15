# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _
# from markdown import markdown
from tagging.fields import TagField, Tag
import tagging

from mptt.models import MPTTModel, TreeForeignKey
from sorl.thumbnail.helpers import ThumbnailError
from sorl.thumbnail.shortcuts import get_thumbnail
from common.models import SeoModel, Pos_Act, Photo
from common.utils import simple_upload_to
from flatpages.models import FlatPage


class CategoryManager(models.Manager):
    def get_query_set(self):
        return super(CategoryManager, self).get_query_set().exclude(is_active=True)


class Category(MPTTModel, SeoModel, Pos_Act):
    CATEGORY_TYPES = (
        ('F', 'Page'),
        ('P', 'Products'),
        ('S', 'Sub categories'),
    )
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    view = models.CharField(max_length=1, choices=CATEGORY_TYPES, default="P")
    name = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True,
                            help_text="Suggested value automatically generated from title. Must be unique.")
    description = models.TextField(blank=True, null=True)
    page = models.ForeignKey(FlatPage, related_name='category_page', verbose_name=u'Страница с описанием', blank=True, null=True)
    image = models.ImageField(upload_to=simple_upload_to('image'), blank=True, null=True)
    # managers
    objects = models.Manager()
    active = CategoryManager()

    def live_entry_set(self):
        return self.product_set.filter(is_active=True)[:6]

    def live_entry(self):
        return self.product_set.filter(is_active=True)

    class Meta:
        ordering = ('position', 'name')
        verbose_name = u'Категория'
        verbose_name_plural = u"Категории"

    def __unicode__(self):
        return self.name

    # @models.permalink
    def get_absolute_url(self):
        if self.view == 'F' and self.page:
            return self.page.get_absolute_url()
        if self.parent:
            return reverse('product_category_parent',
                           kwargs={'parent_slug': self.parent.slug, 'slug': self.slug, })
        return reverse('product_category_list', kwargs={'slug': self.slug})
        # return reverse('product_category_list', (), {'slug': self.slug})

    def admin_thumbnail(self):
        try:
            return '<img src="%s">' % get_thumbnail(self.image, '200').url
            # return '<img src="%s">' % get_thumbnail(self.image, '200x100', crop='center').url
        except IOError:
            return 'IOError'
        except ThumbnailError, ex:
            return 'ThumbnailError, %s' % ex.message

    admin_thumbnail.short_description = (u'Изображение')
    admin_thumbnail.allow_tags = True


class ActiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(ActiveEntryManager, self).get_query_set().filter(is_active=True)


class Product(SeoModel, Pos_Act, models.Model):
    # Core fields.
    name = models.CharField(max_length=250, blank=True, null=True)
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    image = models.ImageField(upload_to=simple_upload_to('product'), blank=True, null=True)
    image_list = generic.GenericRelation(Photo, related_name='product_photo', verbose_name=u'Фото')
    # Metadata.
    featured = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    # Categorization.
    category = TreeForeignKey('Category', null=True, blank=False)
    tags = TagField()

    # Need to be this way around so that non-live entries will show up in Admin, which uses the default (first) manager.
    objects = models.Manager()
    active = ActiveEntryManager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name = u'Продукция'
        verbose_name_plural = u"Продукция"

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('product_detail', (), {'parent_slug': self.category.parent.slug,'slug': self.category.slug, 'pk': self.pk, })

    def admin_thumbnail(self):
        try:
            return '<img src="%s">' % get_thumbnail(self.image, '200').url
            # return '<img src="%s">' % get_thumbnail(self.image, '200x100', crop='center').url
        except IOError:
            return 'IOError'
        except ThumbnailError, ex:
            return 'ThumbnailError, %s' % ex.message

    admin_thumbnail.short_description = (u'Изображение')
    admin_thumbnail.allow_tags = True

    def get_main_photo(self):
        obj = self.image_list.filter(main_image=True).get()
        if obj:
            return obj
        return None

    main_photo = property(get_main_photo)

    def get_photos(self):
        qs = self.image_list.exclude(main_image=True)
        if qs:
            return qs
        return None