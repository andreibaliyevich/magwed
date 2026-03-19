from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import (
    Chat,
    GroupChat,
    Message,
    TextMessage,
    ImageMessage,
    FileMessage,
)


class GroupChatInline(admin.TabularInline):
    """ Group Chat in line for ChatAdmin """
    model = GroupChat
    extra = 0


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    """ Chat Model for admin """
    list_display = ('uuid', 'chat_type')
    radio_fields = {'chat_type': admin.HORIZONTAL}
    inlines = (GroupChatInline,)


class TextMessageInline(admin.TabularInline):
    """ TextMessage in line for MessageAdmin """
    model = TextMessage
    extra = 0


class ImageMessageInline(admin.TabularInline):
    """ ImageMessage in line for MessageAdmin """
    model = ImageMessage
    extra = 0
    readonly_fields = ('get_preview',)

    def get_preview(self, obj):
        return mark_safe(f'<img src="{obj.content.url}" height="100">')
    get_preview.short_description = _('Preview')


class FileMessageInline(admin.TabularInline):
    """ FileMessage in line for MessageAdmin """
    model = FileMessage
    extra = 0


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """ Message Model for admin """
    list_display = ('uuid', 'chat', 'author', 'msg_type', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = (TextMessageInline, ImageMessageInline, FileMessageInline)
