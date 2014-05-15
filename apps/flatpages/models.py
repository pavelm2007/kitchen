# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from sorl.thumbnail.helpers import ThumbnailError
from sorl.thumbnail.shortcuts import get_thumbnail
from common.models import SeoModel, Pos_Act
from common.utils import simple_upload_to

# @python_2_unicode_compatible
class FlatPage(SeoModel, models.Model):
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('title'), max_length=200)
    image = models.ImageField(u'Изображение', upload_to=simple_upload_to('image'), blank=True, null=True)
    content = models.TextField(_('content'), blank=True)
    enable_comments = models.BooleanField(_('enable comments'))
    template_name = models.CharField(_('template name'), max_length=70, blank=True,
        help_text=_("Example: 'flatpages/contact_page.html'. If this isn't provided, the system will use 'flatpages/default.html'."))
    registration_required = models.BooleanField(_('registration required'), help_text=_("If this is checked, only logged-in users will be able to view the page."))
    sites = models.ManyToManyField(Site)

    class Meta:
        db_table = 'django_flatpage'
        verbose_name = _('flat page')
        verbose_name_plural = _('flat pages')
        ordering = ('url',)

    # def __str__(self):
    #     return "%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url

    def get_title(self):
        return self.title

    def get_text(self):
        qs = self.flatpage_block.filter(is_active=True).order_by('position')
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

    article = models.ForeignKey(FlatPage, related_name='flatpage_block', verbose_name=u'Статья')
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
