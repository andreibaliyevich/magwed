from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Notification


class DateCreatedFilter(admin.SimpleListFilter):
    title = _('Date created')
    parameter_name = 'created_at'
    
    def lookups(self, request, model_admin):
        return (
            ('last_days', _('Last day')),
            ('last_week', _('Last week')),
            ('last_month', _('Last month')),
            ('more_month', _('More month')),
        )
    
    def queryset(self, request, queryset):
        val = self.value()
        if val == 'last_days':
            date = timezone.now() - timezone.timedelta(days=1)
            return queryset.filter(created_at__gte=date)
        elif val == 'last_week':
            date = timezone.now() - timezone.timedelta(weeks=1)
            return queryset.filter(created_at__gte=date)
        elif val == 'last_month':
            date = timezone.now() - timezone.timedelta(days=30)
            return queryset.filter(created_at__gte=date)
        elif val == 'more_month':
            date = timezone.now() - timezone.timedelta(days=30)
            return queryset.filter(created_at__lt=date)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """ Notification Model for admin """
    list_display = (
        'uuid',
        'initiator',
        'recipient',
        'reason',
        'viewed',
        'created_at',
    )
    list_filter = (DateCreatedFilter,)
    readonly_fields = ('created_at',)
