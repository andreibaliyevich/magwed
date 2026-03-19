from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class SubjectOfFeedback(IntegerChoices):
    GENERAL = 1, _('General questions and inquiries')
    MODERATION = 2, _('Moderation and deletion of photos')
    TECHNICAL = 3, _('Technical issues')
    PARTNERSHIP = 4, _('Partnership and advertising')
    MESSAGE = 5, _('Message for the administration')
