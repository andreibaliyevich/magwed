from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """ Review Model for admin """
    list_display = ('uuid', 'user', 'author', 'rating', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
