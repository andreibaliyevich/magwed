from rest_framework import permissions
from django.utils.translation import gettext_lazy as _
from .choices import UserType


class UserIsOrganizer(permissions.BasePermission):
    """ User is Organizer """
    message = _('Only organizers have permission.')

    def has_permission(self, request, view):
        return request.user.user_type == UserType.ORGANIZER
