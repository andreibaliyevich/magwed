import uuid
from easy_thumbnails.fields import ThumbnailerImageField
from django.conf import settings
from django.core.files import File
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _
from main.models import Tag
from main.utilities import get_translated_field, get_thumbnail_path
from .choices import CategoryChoices
from .utilities import get_article_path


class Category(models.Model):
    """ Category Model """
    code = models.CharField(
        primary_key=True,
        max_length=16,
        choices=CategoryChoices.choices,
        verbose_name=_('Code'),
    )

    def __str__(self):
        return self.get_code_display()

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['code']


class Article(models.Model):
    """ Article Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name=_('Author'),
    )
    categories = models.ManyToManyField(
        Category,
        related_name='articles',
        verbose_name=_('Categories'),
    )

    title = models.CharField(max_length=128, verbose_name=_('Title'))
    slug = models.SlugField(max_length=128, unique=True, verbose_name=_('Slug'))

    image = models.ImageField(
        upload_to=get_article_path,
        help_text=_('Required minimum of size 1500 x 300.'),
        verbose_name=_('Image'),
    )
    thumbnail = ThumbnailerImageField(
        upload_to=get_thumbnail_path,
        resize_source={
            'size': (1000, 200),
            'crop': 'smart',
            'autocrop': True,
            'quality': 100,
        },
        verbose_name=_('Thumbnail'),
    )

    description = models.CharField(
        max_length=255,
        verbose_name=_('Description'),
    )
    content = models.TextField(verbose_name=_('Content'))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_('Tags'))

    published_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_('Published at'),
    )
    view_count = models.IntegerField(
        default=0,
        verbose_name=_('Count of views'),
    )

    comments = GenericRelation(
        'comments.Comment',
        content_type_field='content_type',
        object_id_field='object_uuid',
    )

    def save(self, *args, **kwargs):
        self.thumbnail = File(self.image)
        super().save(*args, **kwargs)

    def translated_title(self):
        return get_translated_field(self, 'title')

    def translated_description(self):
        return get_translated_field(self, 'description')

    def translated_content(self):
        return get_translated_field(self, 'content')

    def __str__(self):
        return self.translated_title()

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ['-published_at']


class ArticleTranslation(models.Model):
    """ Article Translation Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='translations',
        verbose_name=_('Article'),
    )
    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES[1:],
        verbose_name=_('Language'),
    )

    title = models.CharField(max_length=128, verbose_name=_('Title'))
    description = models.CharField(
        max_length=255,
        verbose_name=_('Description'),
    )
    content = models.TextField(verbose_name=_('Content'))

    class Meta:
        verbose_name = _('Article Translation')
        verbose_name_plural = _('Article Translations')
        ordering = ['article', 'language']
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'language'],
                name='unique_articletranslation',
            )
        ]


class BlogImage(models.Model):
    """ Blog Image Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    file = models.ImageField(upload_to=get_article_path, verbose_name=_('File'))

    class Meta:
        verbose_name = _('Image of Blog')
        verbose_name_plural = _('Images of Blog')
        ordering = ['-uuid']
