import uuid
from easy_thumbnails.fields import ThumbnailerImageField
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _
from main.models import Tag
from main.utilities import get_cover_path, get_thumbnail_path
from .utilities import get_photo_path


class Album(models.Model):
    """ Album Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='albums',
        verbose_name=_('Author'),
    )

    image = models.ImageField(upload_to=get_cover_path, verbose_name=_('Image'))
    thumbnail = ThumbnailerImageField(
        upload_to=get_thumbnail_path,
        resize_source={
            'size': (500, 500),
            'crop': 'smart',
            'autocrop': True,
            'quality': 100,
        },
        verbose_name=_('Thumbnail'),
    )

    title = models.CharField(max_length=128, verbose_name=_('Title'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_('Tags'))

    created_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Count of views'),
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='album_likes',
        verbose_name=_('Likes'),
    )
    rating = models.FloatField(
        default=0,
        verbose_name=_('Rating'),
    )
    editors_choice = models.BooleanField(
        default=False,
        verbose_name=_('Choice of Editors'),
    )

    comments = GenericRelation(
        'comments.Comment',
        content_type_field='content_type',
        object_id_field='object_uuid',
    )
    favorites = GenericRelation(
        'social.Favorite',
        content_type_field='content_type',
        object_id_field='object_uuid',
    )

    class Meta:
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')
        ordering = ['-created_at']


class Photo(models.Model):
    """ Photo Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name=_('Author'),
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='photos',
        verbose_name=_('Album'),
    )

    image = models.ImageField(upload_to=get_photo_path, verbose_name=_('Image'))
    thumbnail = ThumbnailerImageField(
        upload_to=get_thumbnail_path,
        resize_source={
            'size': (500, 500),
            'crop': 'smart',
            'autocrop': True,
            'quality': 100,
        },
        verbose_name=_('Thumbnail'),
    )

    device = models.CharField(
        blank=True,
        max_length=128,
        verbose_name=_('Device'),
    )
    f_number = models.DecimalField(
        blank=True,
        null=True,
        max_digits=5,
        decimal_places=2,
        verbose_name=_('F-number (f/)'),
    )
    exposure_time = models.CharField(
        blank=True,
        max_length=32,
        validators=[
            RegexValidator(
                regex=r'^\d\/\d{1,9}$',
                message=_('Must be entered in the format: 1/123456789.'),
            ),
        ],
        verbose_name=_('Exposure time (s)'),
    )
    focal_length = models.DecimalField(
        blank=True,
        null=True,
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Focal length (mm)'),
    )
    photographic_sensitivity = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Photographic sensitivity (ISO)'),
    )

    title = models.CharField(
        blank=True,
        max_length=128,
        verbose_name=_('Title'),
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_('Tags'))

    uploaded_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_('Uploaded at'),
    )

    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Count of views'),
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='photo_likes',
        verbose_name=_('Likes'),
    )
    rating = models.FloatField(
        default=0,
        verbose_name=_('Rating'),
    )
    editors_choice = models.BooleanField(
        default=False,
        verbose_name=_('Choice of Editors'),
    )

    comments = GenericRelation(
        'comments.Comment',
        content_type_field='content_type',
        object_id_field='object_uuid',
    )
    favorites = GenericRelation(
        'social.Favorite',
        content_type_field='content_type',
        object_id_field='object_uuid',
    )

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')
        ordering = ['-uploaded_at']
