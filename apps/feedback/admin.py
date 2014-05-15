from django.contrib import admin
from feedback.models import Feedback, OrderFeedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message', 'time']
    search_fields = ['email', 'message']
    list_filter = ['time', ]
    date_hierarchy = 'time'
    raw_id_fields = ('user', )


admin.site.register(Feedback, FeedbackAdmin)


class OrderFeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact', 'message', 'time']
    search_fields = ['contact', 'message']
    list_filter = ['time', ]
    date_hierarchy = 'time'
    raw_id_fields = ('user', )


admin.site.register(OrderFeedback, OrderFeedbackAdmin)
