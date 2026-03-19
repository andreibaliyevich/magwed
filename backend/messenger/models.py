import uuid
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from main.validators import MinimumImageSizeValidator
from .choices import ChatType, MessageType
from .utilities import (
    get_chat_path,
    get_image_message_path,
    get_file_message_path,
)


class Chat(models.Model):
    """ Chat Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    chat_type = models.PositiveSmallIntegerField(
        choices=ChatType.choices,
        verbose_name=_('Chat type'),
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chats',
        verbose_name=_('Members'),
    )

    last_message = models.ForeignKey(
        'Message',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='last_message',
        verbose_name=_('Last message'),
    )

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')
        ordering = ['-last_message__created_at']


class GroupChat(models.Model):
    """ Group Chat Model """
    chat = models.OneToOneField(
        Chat,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='group_details',
        verbose_name=_('Chat'),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Owner'),
    )

    name = models.CharField(max_length=150, verbose_name=_('Name'))
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to=get_chat_path,
        validators=[
            FileExtensionValidator(allowed_extensions=('jpg', 'png')),
            MinimumImageSizeValidator(500, 500),
        ],
        help_text=_(
            'Upload JPG or PNG image. '
            'Required minimum of size %(width)d x %(height)d.'
        ) % {
            'width': 500,
            'height': 500,
        },
        verbose_name=_('Image'),
    )

    class Meta:
        verbose_name = _('Group Chat')
        verbose_name_plural = _('Group Chats')
        ordering = ['chat']


class Message(models.Model):
    """ Message Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('Chat'),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_('Author'),
    )

    msg_type = models.PositiveSmallIntegerField(
        choices=MessageType.choices,
        verbose_name=_('Message type'),
    )

    created_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    viewed_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="viewed_messages",
        verbose_name=_('Viewed by'),
    )

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['-created_at']


class TextMessage(models.Model):
    """ Text Message Model """
    message = models.OneToOneField(
        Message,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='text',
        verbose_name=_('Message'),
    )
    content = models.TextField(verbose_name=_('Text content'))

    class Meta:
        verbose_name = _('Text Message')
        verbose_name_plural = _('Text Messages')
        ordering = ['message']


class ImageMessage(models.Model):
    """ Image Message Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('Message'),
    )
    content = models.ImageField(
        upload_to=get_image_message_path,
        verbose_name=_('Image content'),
    )

    class Meta:
        verbose_name = _('Image Message')
        verbose_name_plural = _('Image Messages')
        ordering = ['message']


class FileMessage(models.Model):
    """ File Message Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name=_('Message'),
    )
    content = models.FileField(
        upload_to=get_file_message_path,
        verbose_name=_('File content'),
    )

    class Meta:
        verbose_name = _('File Message')
        verbose_name_plural = _('File Messages')
        ordering = ['message']
