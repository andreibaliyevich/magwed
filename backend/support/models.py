import uuid
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from .choices import SubjectOfFeedback


class Feedback(models.Model):
    """ Feedback Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    subject = models.PositiveSmallIntegerField(
        choices=SubjectOfFeedback.choices,
        verbose_name=_('Subject'),
    )
    email = models.EmailField(verbose_name=_('Email address'))
    comment = models.TextField(verbose_name=_('Comment'))

    created_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedback list')
        ordering = ['-created_at']


class Report(models.Model):
    """ Report Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name=_('Sender'),
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_uuid = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_uuid')

    comment = models.TextField(verbose_name=_('Comment'))
    created_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Report list')
        ordering = ['-created_at']
