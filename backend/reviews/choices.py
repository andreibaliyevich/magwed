from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class RatingOfReview(IntegerChoices):
    FIVE = 5, _('5 stars')
    FOUR = 4, _('4 stars')
    THREE = 3, _('3 stars')
    TWO = 2, _('2 stars')
    ONE = 1, _('1 star')

    __empty__ = _('Choose rating')
