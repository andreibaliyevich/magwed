from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class UserType(IntegerChoices):
    ADMIN = 1, _('Administrator')
    CUSTOMER = 2, _('Customer')
    ORGANIZER = 3, _('Organizer')


class RoleType(IntegerChoices):
    PHOTOGRAPHER = 1, _('Photographer')
    VIDEOGRAPHER = 2, _('Videographer')
    LEADING = 3, _('Leading')
    MUSICIAN = 4, _('Musician')
    DJ = 5, _('DJ')
    AGENCY = 6, _('Agency')
    SALON = 7, _('Salon')
    CONFECTIONERY = 8, _('Confectionery')
    DECORATOR = 9, _('Decorator')
    VISAGISTE = 10, _('Visagiste')
    HAIRDRESSER = 11, _('Hairdresser')

    __empty__ = _('(Unknown)')
