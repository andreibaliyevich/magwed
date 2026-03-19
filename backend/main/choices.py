from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class CurrencyChoices(TextChoices):
    USD = 'USD', _('United States Dollar')
    EUR = 'EUR', _('Euro')
    RUB = 'RUB', _('Russian Ruble')
    BYN = 'BYN', _('Belarusian Ruble')
    UAH = 'UAH', _('Ukrainian Hryvnia')


class CountryChoices(TextChoices):
    BY = 'BY', _('Belarus')
    RU = 'RU', _('Russia')
    UA = 'UA', _('Ukraine')


class CityChoices(TextChoices):    
    BREST_BY = 'Brest-BY', _('Brest (BY)')
    MINSK_BY = 'Minsk-BY', _('Minsk (BY)')

    MOSCOW_RU = 'Moscow-RU', _('Moscow (RU)')
    SAINT_PETERSBURG_RU = 'Saint-Petersburg-RU', _('Saint Petersburg (RU)')

    KYIV_UA = 'Kyiv-UA', _('Kyiv (UA)')
    ODESA_UA = 'Odesa-UA', _('Odesa (UA)')


class LanguageChoices(TextChoices):
    BE = 'be', _('Belarusian')
    EN = 'en', _('English')
    FR = 'fr', _('French')
    DE = 'de', _('German')
    PL = 'pl', _('Polish')
    PT = 'pt', _('Portuguese')
    RU = 'ru', _('Russian')
    UK = 'uk', _('Ukrainian')
