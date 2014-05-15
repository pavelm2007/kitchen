# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
# from markdown import markdown
from tagging.fields import TagField, Tag
import tagging

from sorl.thumbnail.helpers import ThumbnailError
from sorl.thumbnail.shortcuts import get_thumbnail
from common.models import SeoModel, Pos_Act
from common.utils import simple_upload_to


class Category(models.Model):
    pass
    # title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    # slug = models.SlugField(unique=True,
    #                         help_text="Suggested value automatically generated from title. Must be unique.")
    # description = models.TextField()
    #
    # def live_entry_set(self):
    #     from coltrane.models import Entry
    #
    #     return self.entry_set.filter(status=Entry.LIVE_STATUS)
    #
    # class Meta:
    #     ordering = ['title']
    #     verbose_name_plural = "Categories"
    #
    # def __unicode__(self):
    #     return self.title
    #
    # @models.permalink
    # def get_absolute_url(self):
    #     return ('coltrane_category_detail', (), {'slug': self.slug})


class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)



class Entry(SeoModel, models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, u'Оубликовано'),
        (DRAFT_STATUS, u'В работе'),
        (HIDDEN_STATUS, u'Скрыто'),
    )

    # category = models.ManyToManyField(Category, related_name='articles', verbose_name=u'Категория', blank=True, null=True)
    source_data = models.CharField(u'Источник', max_length=250, blank=True, null=True)
    title = models.CharField(u'Заголовок', max_length=255)
    short_title = models.CharField(u'Заголок в ленте', max_length=160, blank=True, null=True)
    slug = models.SlugField(u'Slug', unique_for_date='pub_date')
    pub_date = models.DateField(u'Дата публикации', default=datetime.datetime.now())
    pub_time = models.TimeField(u'Время публикации', default=datetime.datetime.now())
    short_text = models.TextField(u'Анонс', blank=True, null=True)
    text = models.TextField(u'Текст')
    image = models.ImageField(u'Главное фото', upload_to=simple_upload_to('image'), blank=True, null=True)
    status = models.IntegerField(u'Статус', choices=STATUS_CHOICES, default=LIVE_STATUS)

    objects = models.Manager()
    live = LiveEntryManager()

    class Meta:
        ordering = ['-pub_date', '-pub_time', '-id', ]
        verbose_name = u'Статья'
        verbose_name_plural = u'Статьи'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('entry_detail', (), {'slug': self.slug,})

    def get_text(self):
        qs = self.article_block.filter(is_active=True).order_by('position')
        block_count = qs.count()
        bl = []
        if qs:
            it = 0
            i = 0
            while i < block_count:
                type = qs[i].block_type
                if type in qs[i].CAN_COLLAPSE:
                    res = []
                    it = i
                    for j in qs[i:]:
                        if j.block_type == type:
                            res.append(j)
                            it += 1
                        else:
                            break
                    bl.append([type, res])
                    # bl.append([type, {'blocks':res}])
                    i = it - 1
                else:
                    bl.append([type, qs[i]])
                i += 1
        return bl

    def get_links(self):
        return self.article_block.filter(block_type=7).order_by('position')

    def admin_thumbnail(self):
        try:
            return '<img src="%s">' % get_thumbnail(self.image, '200x100', crop='center').url
        except IOError:
            return 'IOError'
        except ThumbnailError, ex:
            return 'ThumbnailError, %s' % ex.message

    admin_thumbnail.short_description = (u'Главное фото')
    admin_thumbnail.allow_tags = True


class Block(Pos_Act, models.Model):
    BLOCK_TYPES = (
        (1, u'Текст'),
        (2, u'Текст - Фото'),
        (3, u'Фото - Текст'),
        (4, u'Фото - Фото'),
        (5, u'Галерея'),

    )
    CAN_COLLAPSE = (5,)

    article = models.ForeignKey(Entry, related_name='article_block', verbose_name=u'Статья')
    block_type = models.IntegerField(u'Тип блока', choices=BLOCK_TYPES, default=1)

    title = models.CharField(u'Заголовок', max_length=255, blank=True, null=True)
    text = models.TextField(u'Текст', blank=True, null=True)
    image = models.ImageField(u'Фото', upload_to=simple_upload_to('image'), blank=True, null=True)

    class Meta:
        verbose_name = u'Блок'
        verbose_name_plural = u'Блоки'
        ordering = ['position', ]

    def get_album_photo(self):
        return self.album.images.all()

    album_photo = property(get_album_photo)

