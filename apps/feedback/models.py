# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


__all__ = ['Feedback', ]


class Feedback(models.Model):
    position = models.SmallIntegerField(u'Позиция', default=100)
    is_active = models.BooleanField(u'Видимость', default=False)
    user = models.ForeignKey(User, blank=True, null=True,
                             verbose_name=_('User'))
    name = models.CharField(u'Ваше имя', max_length=75)
    email = models.CharField(U'Email или номер телефона', max_length=90)
    message = models.TextField(u'Сообщение')
    time = models.DateTimeField(u'Время', auto_now_add=True)

    class Meta:
        ordering = ['position','-time']
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')

    def __unicode__(self):
        return self.message

    def get_absolute_url(self):
        return reverse('admin:view-feedback', args=[self.id])


class OrderFeedback(models.Model):
    user = models.ForeignKey(User, blank=True, null=True,
                             verbose_name=_('User'))
    name = models.CharField(u'Ваше имя', max_length=75)
    contact = models.CharField(U'Номер телефона', max_length=20)
    message = models.TextField(u'Задайте вопрос мастеру, и укажите удобное время для того чтобы он перезвонил. Спасибо.',)
    time = models.DateTimeField(u'Время', auto_now_add=True)

    class Meta:
        ordering = ['-time']
        verbose_name = _('Order Feedback')
        verbose_name_plural = _('Order Feedbacks')

    def __unicode__(self):
        return self.message

    def get_absolute_url(self):
        return reverse('admin:view-orderfeedback', args=[self.id])
