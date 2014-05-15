# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model
# from markdown import markdown
from tagging.fields import TagField, Tag

from mptt.models import MPTTModel, TreeForeignKey
from sorl.thumbnail.helpers import ThumbnailError
from sorl.thumbnail.shortcuts import get_thumbnail
from common.models import SeoModel, Pos_Act, Photo
from common.utils import simple_upload_to
from flatpages.models import FlatPage

ITEM_CONTENT_TYPES = SortedDict([# 'model_name': {'name': 'user_friendly_name', 'class': 'class_name'}
                                 ('project', {'name': u'Проекты', }),
                                 ('works', {'name': u'Пример работы', }),
                                 ('facade', {'name': u'Фасад', }),
                                 ('millingfacade', {'name': u'Фрезеровка фасада', }),
                                 ('finding', {'name': u'Фурнитура', }),
                                 ('ldsp', {'name': u'ЛДСП', }),
                                 ('tabletop', {'name': u'Столешница', }),
                                 ('photoprinting', {'name': u'Фото печать', }),
])
items_content_types_filters = {
    'app_label': 'catalog',
    'model__in': ITEM_CONTENT_TYPES.keys(),
}


class Country(models.Model):
    name = models.CharField(u'Название', max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'


class Producer(SeoModel, Pos_Act, models.Model):
    name = models.CharField(u'Название', max_length=100)
    country = models.ForeignKey('Country', verbose_name=u'Страна')
    discount = models.PositiveSmallIntegerField(u'Скидка (%)', blank=True, null=True)
    image = models.ImageField(u'Логотип',
                              upload_to=simple_upload_to('image'),
                              blank=True
    )
    description = models.TextField(u'Описание')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = u'Производитель'
        verbose_name_plural = u'Производители'

        # def get_absolute_url(self):
        #     abs_url = getattr(self, '_abs_url', None)
        #     if abs_url is None:
        #         self._abs_url = reverse('catalog_producers_detail', args=[str(self.id)])
        #     return self._abs_url


class CategoryManager(models.Manager):
    def get_query_set(self):
        return super(CategoryManager, self).get_query_set().exclude(is_active=False)


class Category(MPTTModel, SeoModel, Pos_Act):
    CATEGORY_TYPES = (
        ('F', 'Page'),
        ('P', 'Products'),
        ('S', 'Sub categories'),
    )
    content_type = models.ForeignKey(ContentType, verbose_name=u'Тип товара',
                                     limit_choices_to=items_content_types_filters, blank=True, null=True)
    content_type_model = models.CharField(u'Название', editable=False, blank=True, null=True, max_length=30)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    view = models.CharField(max_length=1, choices=CATEGORY_TYPES, default="P")
    name = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True,
                            help_text="Suggested value automatically generated from title. Must be unique.")
    description = models.TextField(blank=True, null=True)
    page = models.ForeignKey(FlatPage, related_name='category_page', verbose_name=u'Страница с описанием', blank=True,
                             null=True)
    image = models.ImageField(upload_to=simple_upload_to('image'), blank=True, null=True)
    # managers
    objects = models.Manager()
    active = CategoryManager()


    def live_entry_set(self):
        if not self.parent:
            qs = self.get_children(is_active=True)
            return qs
        return None

    def live_entry(self):
        if not self.parent:
            qs = self.get_children(is_active=True)
            return qs
        return None

    class Meta:
        ordering = ('position', 'name')
        verbose_name = u'Категория'
        verbose_name_plural = u"Категории"

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.content_type:
            self.content_type_model = self.content_type.model
        super(Category, self).save(*args, **kwargs)

        # @models.permalink

    def get_absolute_url(self):
        if self.view == 'F' and self.page:
            return self.page.get_absolute_url()
            # if self.content_type_model == 'works':
        #     return reverse('catalog:works_detail',
        #                    kwargs={'model_name': self.content_type_model, 'slug': self.slug,})
        # if self.slug == 'proekty':
        #     return reverse('catalog:category_detail', kwargs={'model_name': self.slug,})
        # if self.parent == 'proekty':
        #     return reverse('catalog:work_category_detail',
        #                    kwargs={'model_name': self.parent.slug, 'slug': self.slug, })
        if self.content_type_model == 'works' or self.content_type_model == 'project':
            return reverse('catalog:work_category_detail',
                           kwargs={'model_name': self.content_type_model, 'slug': self.slug, })
            # if self.content_type_model == 'project':
        #     return reverse('catalog:work_category_detail',
        #                    kwargs={'model_name': self.content_type_model, 'slug': self.slug, })
        if self.parent:
            return reverse('catalog:category_detail',
                           kwargs={'model_name': self.content_type_model, })

        return reverse('catalog:category_detail',
                       kwargs={'model_name': self.slug, })

        #                kwargs={'model_name': self.slug})
        # return reverse('catalog:materials_detail', kwargs={'slug': self.slug})

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

    def items_count(self):
        model_name = self.content_type.model
        model = get_model('catalog', model_name)
        qs = model.objects.filter(is_active=True).filter(category__slug=self.slug)
        return qs.count()


class ActiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(ActiveEntryManager, self).get_query_set().filter(is_active=True)


class BaseProduct(SeoModel, Pos_Act, models.Model):
    # Core fields.
    name = models.CharField(max_length=250, blank=True)
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    image = models.ImageField(upload_to=simple_upload_to('image'), blank=True, null=True)
    image_list = generic.GenericRelation(Photo, verbose_name=u'Фото')
    # Metadata.
    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique_for_date='pub_date', blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    # Categorization.
    category = models.ForeignKey('Category')
    tags = TagField()

    # Need to be this way around so that non-live entries will show up in Admin, which uses the default (first) manager.
    objects = models.Manager()
    active = ActiveEntryManager()

    class Meta:
        abstract = True
        ordering = ['position', '-id', '-pub_date']
        verbose_name = u'Продукция'
        verbose_name_plural = u"Продукция"

    def __unicode__(self):
        return '%s - %s' % (self.image, self.pk)
        # return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('catalog:item_detail', (), {'model_name': self.category.content_type_model, 'pk': self.pk, })

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


class Works(BaseProduct):
    class Meta:
        ordering = ['position', '-id']
        verbose_name = u'Пример работы'
        verbose_name_plural = u'Примеры работ'

    @models.permalink
    def get_absolute_url(self):
        return ('catalog:work_detail', (), dict(model_name=u'works', slug=self.category.slug, pk=self.pk))


class Project(BaseProduct):
    class Meta:
        ordering = ['position', '-id']
        verbose_name = u'Проект'
        verbose_name_plural = u'Проекты'

    @models.permalink
    def get_absolute_url(self):
        return ('catalog:work_detail', (), dict(model_name=u'project', slug=self.category.slug, pk=self.pk))


class Facade(BaseProduct):
    class Meta:
        ordering = ['position', '-id']
        verbose_name = u'Фасад'
        verbose_name_plural = u'Фасады'


class MillingFacade(BaseProduct):
    class Meta:
        ordering = ['position', '-id']
        verbose_name = u'Фрезеровка фасада'
        verbose_name_plural = u'Фрезеровка фасадов'


class Finding(BaseProduct):
    class Meta:
        ordering = ['position', '-id']
        verbose_name = u'Фурнитура'
        verbose_name_plural = u'Фурнитура'


class Ldsp(BaseProduct):
    class Meta:
        ordering = ['position', '-id']
        verbose_name = u'ЛДСП'
        verbose_name_plural = u'ЛДСП'


class Tabletop(BaseProduct):
    class Meta:
        ordering = ['position', '-id']
        verbose_name = u'Столешница'
        verbose_name_plural = u'Столешницы'


class PhotoPrinting(BaseProduct):
    class Meta:
        ordering = ['position', '-id']
        verbose_name = u'Фото печать'
        verbose_name_plural = u'Фото печать'

