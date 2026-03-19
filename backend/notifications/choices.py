from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class ReasonOfNotification(IntegerChoices):
    FOLLOW = 1, _('New follow')
    ARTICLE = 2, _('New article')
    ALBUM = 3, _('New album')
    PHOTO = 4, _('New photo')
    LIKE_ALBUM = 5, _('Like of album')
    LIKE_PHOTO = 6, _('Like of photo')
    COMMENT = 7, _('New comment')
    REVIEW = 8, _('New review')
    MESSAGE = 9, _('New message')
