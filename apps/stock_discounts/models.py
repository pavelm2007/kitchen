# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
# from markdown import markdown
from tagging.fields import TagField, Tag
import tagging

from sorl.thumbnail.helpers import ThumbnailError
from sorl.thumbnail.shortcuts import get_thumbnail
from common.models import SeoModel, Pos_Act, Photo
from common.utils import simple_upload_to


class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(is_active=True)


class Product(SeoModel,Pos_Act, models.Model):
    STOCK_STATUS = 1
    DISCOUNT_STATUS = 2
    TYPE_CHOICES = (
        (STOCK_STATUS, u'Скидки'),
        (DISCOUNT_STATUS, u'Акции'),
    )

    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )

    # Core fields.
    title = models.CharField(max_length=250)
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    image = models.ImageField(upload_to=simple_upload_to('image'))
    image_list = generic.GenericRelation(Photo, related_name='stock_discount_photo', verbose_name=u'Фото')
    # Metadata.
    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique_for_date='pub_date')
    type_category = models.IntegerField(u'Тип категории', choices=TYPE_CHOICES, default=STOCK_STATUS)
    # Categorization.
    # category = models.ForeignKey(Category)
    tags = TagField()

    # Need to be this way around so that non-live entries will show up in Admin, which uses the default (first) manager.
    objects = models.Manager()
    active = LiveEntryManager()

    class Meta:
        ordering = ['position', '-pub_date']
        verbose_name = u'Специальное предложение'
        verbose_name_plural = u"Специальные предложения"

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('stock_discount_detail', (), {'slug': self.slug,})

    def get_type_cat(self):
        for key, value in self.TYPE_CHOICES:
            if int(self.type_category)==int(key):
                cat_name = value
                cat_url = reverse('stock_discount_sub_list', kwargs={'type': key})
                return {'current_category': cat_name,'current_url': cat_url,}

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
        qs = self.image_list.all()
        if qs:
            return qs
        return None