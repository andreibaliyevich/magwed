from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class CategoryChoices(TextChoices):
    DESIGN = 'design', _('Design')
    FASHION = 'fashion', _('Fashion')
    INSPIRATION = 'inspiration', _('Inspiration')
    JOURNEY = 'journey', _('Journey')
    LIFESTYLE = 'lifestyle', _('Lifestyle')
    PHOTOGRAPHY = 'photography', _('Photography')
    TECHNOLOGY = 'technology', _('Technology')
    WEDDING = 'wedding', _('Wedding')

    __empty__ = _('(Unknown)')
