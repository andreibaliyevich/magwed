from rest_framework import permissions
from django.utils.translation import gettext_lazy as _


class UserIsAuthor(permissions.BasePermission):
    """ User is Author """
    message = _('Only author have permission.')

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
