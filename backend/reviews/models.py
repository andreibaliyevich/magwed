import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from .choices import RatingOfReview


class Review(models.Model):
    """ Review Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_reviews',
        verbose_name=_('User'),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='author_reviews',
        verbose_name=_('Author'),
    )

    rating = models.IntegerField(
        choices=RatingOfReview.choices,
        verbose_name=_('Rating'),
    )
    comment = models.TextField(verbose_name=_('Comment'))

    created_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_review',
            )
        ]
