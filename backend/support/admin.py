from django.contrib import admin
from .models import Feedback, Report


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """ Feedback Model for admin """
    list_display = ('uuid', 'subject', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """ Report Model for admin """
    list_display = ('uuid', 'sender', 'created_at')
    readonly_fields = ('created_at',)