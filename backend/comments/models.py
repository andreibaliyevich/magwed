import uuid
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import (
    GenericRelation,
    GenericForeignKey,
)
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    """ Comment Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_uuid = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_uuid')

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Author'),
    )

    content = models.TextField(verbose_name=_('Content'))

    created_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    comments = GenericRelation(
        'self',
        content_type_field='content_type',
        object_id_field='object_uuid',
    )

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['created_at']
        indexes = [
            models.Index(
                fields=['content_type', 'object_uuid'],
                name='comment_index',
            )
        ]
