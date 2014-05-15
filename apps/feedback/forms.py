# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets
from .models import Feedback, OrderFeedback


class FeedbackForm(forms.ModelForm):
    message = forms.CharField(widget=widgets.Textarea(attrs={'placeholder': u'Ваше сообщение', 'class': 'span9', }))

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['email'].widget.attrs['class'] = 'span4'
            self.fields['name'].widget.attrs['class'] = 'span4'
            self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label
            self.fields['name'].widget.attrs['placeholder'] = self.fields['name'].label


    class Meta:
        model = Feedback
        exclude = ('user','position', 'is_active')


class OrderFeedbackForm(forms.ModelForm):
    message = forms.CharField(widget=widgets.Textarea(attrs={'placeholder': u'Ваше сообщение', 'class': 'span5', 'rows':'5',}))

    def __init__(self, *args, **kwargs):
        super(OrderFeedbackForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['contact'].widget.attrs['class'] = 'span5'
            self.fields['name'].widget.attrs['class'] = 'span5'
            self.fields['contact'].widget.attrs['placeholder'] = self.fields['contact'].label
            self.fields['name'].widget.attrs['placeholder'] = self.fields['name'].label


    class Meta:
        model = OrderFeedback
        exclude = ('user',)
