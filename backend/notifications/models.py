import uuid
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from .choices import ReasonOfNotification


class Notification(models.Model):
    """ Notification Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    initiator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='initiator_notifications',
        verbose_name=_('Initiator'),
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipient_notifications',
        verbose_name=_('Recipient'),
    )

    reason = models.PositiveSmallIntegerField(
        choices=ReasonOfNotification.choices,
        verbose_name=_('Reason'),
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_uuid = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_uuid')

    created_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    viewed = models.BooleanField(default=False, verbose_name=_('Viewed'))

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']
