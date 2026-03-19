from rest_framework import permissions
from django.utils.translation import gettext_lazy as _
from .choices import ChatType


class ChatIsGroupChat(permissions.BasePermission):
    """ Chat Is Group Chat """
    message = _('This chat is not a group chat.')

    def has_object_permission(self, request, view, obj):
        return obj.chat_type == ChatType.GROUP


class ChatDestroyPermission(permissions.BasePermission):
    """ Chat Destroy Permission """
    message = _('You cannot delete this chat.')

    def has_object_permission(self, request, view, obj):
        if obj.chat_type == ChatType.DIALOG:
            return True
        if (obj.chat_type == ChatType.GROUP
                and obj.group_details.owner == request.user):
            return True
        return False
