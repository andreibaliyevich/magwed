from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """ Comment Model for admin """
    list_display = ('uuid', 'content_type', 'author', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
