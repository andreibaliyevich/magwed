import uuid
from decimal import Decimal
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.validators import MinValueValidator
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from .choices import (
    CurrencyChoices,
    CountryChoices,
    CityChoices,
    LanguageChoices,
)
from .utilities import get_magazine_path
from .validators import MinimumImageSizeValidator


class Currency(models.Model):
    """ Currency Model """
    code = models.CharField(
        primary_key=True,
        max_length=3,
        choices=CurrencyChoices.choices,
        verbose_name=_('Code'),
    )
    conversion_rate = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        default=0.0000,
        validators=[MinValueValidator(Decimal('0.0000'))],
        verbose_name=_('Conversion rate'),
    )

    def __str__(self):
        return self.get_code_display()

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')
        ordering = ['code']


class Country(models.Model):
    """ Country Model """
    code = models.CharField(
        primary_key=True,
        max_length=2,
        choices=CountryChoices.choices,
        verbose_name=_('Code'),
    )

    def __str__(self):
        return self.get_code_display()

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ['code']


class City(models.Model):
    """ City Model """
    code = models.CharField(
        primary_key=True,
        max_length=32,
        choices=CityChoices.choices,
        verbose_name=_('Code'),
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='cities',
        verbose_name=_('Country'),
    )

    def __str__(self):
        return self.get_code_display()

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        ordering = ['code']


class Language(models.Model):
    """ Language Model """
    code = models.CharField(
        primary_key=True,
        max_length=2,
        choices=LanguageChoices.choices,
        verbose_name=_('Code'),
    )

    def __str__(self):
        return self.get_code_display()

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        ordering = ['code']


class Magazine(models.Model):
    """ Magazine Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    title = models.CharField(max_length=64, verbose_name=_('Title'))
    slug = models.SlugField(unique=True, max_length=64, verbose_name=_('Slug'))

    image = ThumbnailerImageField(
        upload_to=get_magazine_path,
        validators=[
            FileExtensionValidator(allowed_extensions=('jpg', 'png')),
            MinimumImageSizeValidator(500, 650),
        ],
        resize_source={
            'size': (500, 650),
            'crop': 'smart',
            'autocrop': True,
            'quality': 100,
        },
        help_text=_(
            'Upload JPG or PNG image. '
            'Required minimum of size %(width)d x %(height)d.'
        ) % {
            'width': 500,
            'height': 650,
        },
        verbose_name=_('Image'),
    )
    file = models.FileField(
        upload_to=get_magazine_path,
        validators=[
            FileExtensionValidator(allowed_extensions=('pdf',)),
        ],
        verbose_name=_('File'),
    )

    published_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_('Published at'),
    )

    def __str__(self):
        return f'{self.title} | {self.published_at}'

    class Meta:
        verbose_name = _('Magazine')
        verbose_name_plural = _('Magazines')
        ordering = ['-published_at']


class Tag(models.Model):
    """ Tag Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(unique=True, max_length=64, verbose_name=_('Name'))
    created_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['-created_at']
