from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class ChatType(IntegerChoices):
    DIALOG = 1, _('Dialog')
    GROUP = 2, _('Group')


class MessageType(IntegerChoices):
    TEXT = 1, _('Text')
    IMAGES = 2, _('Images')
    FILES = 3, _('Files')
