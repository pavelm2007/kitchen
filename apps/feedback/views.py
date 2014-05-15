# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string

from annoying.decorators import JsonResponse

from .forms import FeedbackForm, OrderFeedbackForm


class Sended(TemplateView):
    template_name = 'feedback/feedback_sended.html'


class Comment(TemplateView):
    template_name = 'feedback/comment.html'


def leave_feedback(request):
    form = FeedbackForm(request.GET or None)
    if form.is_valid():
        feedback = form.save(commit=False)
        if request.user.is_authenticated():
            feedback.user = request.user
        feedback.save()

        if request.is_ajax():
            return JsonResponse({'status': True})
        elif not getattr(settings, 'FEEDBACK_ON_SINGLE_PAGE', True):
            from django.contrib import messages

            messages.add_message(request, messages.INFO,
                                 _("Your feedback has been saved successfully."))
            next_ = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
        else:
            next_ = reverse('feedback_sended')
        return HttpResponseRedirect(next_)

    if request.is_ajax():
        return JsonResponse({'status': False, 'errors': form.errors})
    return render_to_response('feedback/comment.html', {'feedback_form': form},
                              context_instance=RequestContext(request))
    # return render_to_response('feedback/feedback_form.html', {'form': form},
    #                           context_instance=RequestContext(request))


def order_feedback(request):
    form = OrderFeedbackForm(request.POST or None)
    if form.is_valid():
        fields = form.cleaned_data
        feedback = form.save(commit=False)
        if request.user.is_authenticated():
            feedback.user = request.user
        feedback.save()
        message_context = {
            'name': fields['name'],
            'contact': fields['contact'],
            'message': fields['message'],
            'time': str(datetime.datetime.now()),
        }
        mail_message = render_to_string('feedback/order_client.txt', message_context)
        managers = [manager[1] for manager in settings.MANAGERS]
        send_mail(u'Новый ЗАКАЗ', mail_message, settings.EMAIL_FROM,
                  managers, fail_silently=False)

        if request.is_ajax():
            return JsonResponse({'status': True})

    if request.is_ajax():
        return JsonResponse({'status': False, 'errors': form.errors})
