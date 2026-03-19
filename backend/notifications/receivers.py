from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import caches
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from blog.models import Article
from blog.serializers import ArticleBriefReadSerializer
from comments.models import Comment
from comments.serializers import CommentShortReadSerializer
from messenger.models import Message
from messenger.serializers import MessageBriefReadSerializer
from messenger.signals import msg_saved
from portfolio.models import Album, Photo
from portfolio.serializers import (
    AlbumShortReadSerializer,
    PhotoShortReadSerializer,
)
from portfolio.signals import like_obj, dislike_obj
from reviews.models import Review
from reviews.serializers import ReviewShortReadSerializer
from social.models import Follow
from .choices import ReasonOfNotification
from .models import Notification
from .serializers import NotificationShortSerializer


channel_layer = get_channel_layer()


@receiver(post_save, sender=Follow)
def follow_saved(sender, instance, created, **kwargs):
    """ Save and send follow notification """
    notice = Notification.objects.create(
        initiator=instance.follower,
        recipient=instance.user,
        reason=ReasonOfNotification.FOLLOW,
        content_object=instance,
    )

    notice_data = NotificationShortSerializer(notice).data
    if notice_data['initiator']['avatar']:
        avatar_url = notice_data['initiator']['avatar']
        notice_data['initiator']['avatar'] = f'{settings.API_URL}{avatar_url}'
    notice_data['content_object'] = None

    async_to_sync(channel_layer.group_send)(
        f'notification-{notice.recipient.uuid}',
        {
            'type': 'send_json_data',
            'action': 'created',
            'data': notice_data,
        }
    )


@receiver(pre_delete, sender=Follow)
def follow_deleting(sender, instance, **kwargs):
    """ Delete and send follow notification """
    notice = Notification.objects.filter(
        initiator=instance.follower,
        recipient=instance.user,
        reason=ReasonOfNotification.FOLLOW,
        content_type=ContentType.objects.get_for_model(Follow),
        object_uuid=instance.uuid,
    ).first()
    if notice is not None:
        notice_uuid = str(notice.uuid)
        notice.delete()
        async_to_sync(channel_layer.group_send)(
            f'notification-{instance.user.uuid}',
            {
                'type': 'send_json_data',
                'action': 'deleted',
                'data': notice_uuid,
            }
        )


@receiver(post_save, sender=Article)
def article_saved(sender, instance, created, **kwargs):
    """ Save and send article notification """
    if created:
        for follow in instance.author.followers.all():
            notice = Notification.objects.create(
                initiator=instance.author,
                recipient=follow.follower,
                reason=ReasonOfNotification.ARTICLE,
                content_object=instance,
            )

            notice_data = NotificationShortSerializer(notice).data
            if notice_data['initiator']['avatar']:
                avatar_url = notice_data['initiator']['avatar']
                notice_data['initiator']['avatar'] = f'{settings.API_URL}{avatar_url}'

            notice_data['content_object'] = ArticleBriefReadSerializer(instance).data
            thumbnail_url = notice_data['content_object']['thumbnail']
            notice_data['content_object']['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

            async_to_sync(channel_layer.group_send)(
                f'notification-{notice.recipient.uuid}',
                {
                    'type': 'send_json_data',
                    'action': 'created',
                    'data': notice_data,
                }
            )
    else:
        content_object_data = ArticleBriefReadSerializer(instance).data
        thumbnail_url = content_object_data['thumbnail']
        content_object_data['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

        notices_values = Notification.objects.filter(
            initiator=instance.author,
            reason=ReasonOfNotification.ARTICLE,
            content_type=ContentType.objects.get_for_model(Article),
            object_uuid=instance.uuid,
        ).values('uuid', 'recipient__uuid')

        for value in notices_values:
            async_to_sync(channel_layer.group_send)(
                f"notification-{value['recipient__uuid']}",
                {
                    'type': 'send_json_data',
                    'action': 'updated',
                    'data': {
                        'uuid': str(value['uuid']),
                        'content_object': content_object_data,
                    },
                }
            )


@receiver(pre_delete, sender=Article)
def article_deleting(sender, instance, **kwargs):
    """ Delete and send article notification """
    notices = Notification.objects.filter(
        initiator=instance.author,
        reason=ReasonOfNotification.ARTICLE,
        content_type=ContentType.objects.get_for_model(Article),
        object_uuid=instance.uuid,
    )
    values_list = list(notices.values('uuid', 'recipient__uuid'))
    notices.delete()
    for value in values_list:
        async_to_sync(channel_layer.group_send)(
            f"notification-{value['recipient__uuid']}",
            {
                'type': 'send_json_data',
                'action': 'deleted',
                'data': str(value['uuid']),
            }
        )


@receiver(post_save, sender=Album)
def album_saved(sender, instance, created, **kwargs):
    """ Save and send album notification """
    if created:
        for follow in instance.author.followers.all():
            notice = Notification.objects.create(
                initiator=instance.author,
                recipient=follow.follower,
                reason=ReasonOfNotification.ALBUM,
                content_object=instance,
            )

            notice_data = NotificationShortSerializer(notice).data
            if notice_data['initiator']['avatar']:
                avatar_url = notice_data['initiator']['avatar']
                notice_data['initiator']['avatar'] = f'{settings.API_URL}{avatar_url}'

            notice_data['content_object'] = AlbumShortReadSerializer(instance).data
            thumbnail_url = notice_data['content_object']['thumbnail']
            notice_data['content_object']['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

            async_to_sync(channel_layer.group_send)(
                f'notification-{notice.recipient.uuid}',
                {
                    'type': 'send_json_data',
                    'action': 'created',
                    'data': notice_data,
                }
            )
    else:
        content_object_data = AlbumShortReadSerializer(instance).data
        thumbnail_url = content_object_data['thumbnail']
        content_object_data['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

        notices_values = Notification.objects.filter(
            initiator=instance.author,
            reason=ReasonOfNotification.ALBUM,
            content_type=ContentType.objects.get_for_model(Album),
            object_uuid=instance.uuid,
        ).values('uuid', 'recipient__uuid')

        for value in notices_values:
            async_to_sync(channel_layer.group_send)(
                f"notification-{value['recipient__uuid']}",
                {
                    'type': 'send_json_data',
                    'action': 'updated',
                    'data': {
                        'uuid': str(value['uuid']),
                        'content_object': content_object_data,
                    },
                }
            )


@receiver(pre_delete, sender=Album)
def album_deleting(sender, instance, **kwargs):
    """ Delete and send album notification """
    notices = Notification.objects.filter(
        content_type=ContentType.objects.get_for_model(Album),
        object_uuid=instance.uuid,
    )
    values_list = list(notices.values('uuid', 'recipient__uuid'))
    notices.delete()
    for value in values_list:
        async_to_sync(channel_layer.group_send)(
            f"notification-{value['recipient__uuid']}",
            {
                'type': 'send_json_data',
                'action': 'deleted',
                'data': str(value['uuid']),
            }
        )


@receiver(post_save, sender=Photo)
def photo_saved(sender, instance, created, **kwargs):
    """ Save and send photo notification """
    if instance.album is None:
        if created:
            for follow in instance.author.followers.all():
                notice = Notification.objects.create(
                    initiator=instance.author,
                    recipient=follow.follower,
                    reason=ReasonOfNotification.PHOTO,
                    content_object=instance,
                )

                notice_data = NotificationShortSerializer(notice).data
                if notice_data['initiator']['avatar']:
                    avatar_url = notice_data['initiator']['avatar']
                    notice_data['initiator']['avatar'] = f'{settings.API_URL}{avatar_url}'

                notice_data['content_object'] = PhotoShortReadSerializer(instance).data
                thumbnail_url = notice_data['content_object']['thumbnail']
                notice_data['content_object']['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

                async_to_sync(channel_layer.group_send)(
                    f'notification-{notice.recipient.uuid}',
                    {
                        'type': 'send_json_data',
                        'action': 'created',
                        'data': notice_data,
                    }
                )
        else:
            content_object_data = PhotoShortReadSerializer(instance).data
            thumbnail_url = content_object_data['thumbnail']
            content_object_data['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

            notices_values = Notification.objects.filter(
                initiator=instance.author,
                reason=ReasonOfNotification.PHOTO,
                content_type=ContentType.objects.get_for_model(Photo),
                object_uuid=instance.uuid,
            ).values('uuid', 'recipient__uuid')

            for value in notices_values:
                async_to_sync(channel_layer.group_send)(
                    f"notification-{value['recipient__uuid']}",
                    {
                        'type': 'send_json_data',
                        'action': 'updated',
                        'data': {
                            'uuid': str(value['uuid']),
                            'content_object': content_object_data,
                        },
                    }
                )


@receiver(pre_delete, sender=Photo)
def photo_deleting(sender, instance, **kwargs):
    """ Delete and send photo notification """
    if instance.album is None:
        notices = Notification.objects.filter(
            content_type=ContentType.objects.get_for_model(Photo),
            object_uuid=instance.uuid,
        )
        values_list = list(notices.values('uuid', 'recipient__uuid'))
        notices.delete()
        for value in values_list:
            async_to_sync(channel_layer.group_send)(
                f"notification-{value['recipient__uuid']}",
                {
                    'type': 'send_json_data',
                    'action': 'deleted',
                    'data': str(value['uuid']),
                }
            )


@receiver(like_obj, sender=Album)
def album_liked(sender, instance, user, **kwargs):
    """ Save and send album liked notification """
    if instance.author.uuid != user.uuid:
        notice = Notification.objects.create(
            initiator=user,
            recipient=instance.author,
            reason=ReasonOfNotification.LIKE_ALBUM,
            content_object=instance,
        )

        notice_data = NotificationShortSerializer(notice).data
        if notice_data['initiator']['avatar']:
            avatar_url = notice_data['initiator']['avatar']
            notice_data['initiator']['avatar'] = f'{settings.API_URL}{avatar_url}'

        notice_data['content_object'] = AlbumShortReadSerializer(instance).data
        thumbnail_url = notice_data['content_object']['thumbnail']
        notice_data['content_object']['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

        async_to_sync(channel_layer.group_send)(
            f'notification-{notice.recipient.uuid}',
            {
                'type': 'send_json_data',
                'action': 'created',
                'data': notice_data,
            }
        )


@receiver(dislike_obj, sender=Album)
def album_disliked(sender, instance, user, **kwargs):
    """ Delete and send album disliked notification """
    if instance.author.uuid != user.uuid:
        notice = Notification.objects.filter(
            initiator=user,
            recipient=instance.author,
            reason=ReasonOfNotification.LIKE_ALBUM,
            content_type=ContentType.objects.get_for_model(Album),
            object_uuid=instance.uuid,
        ).first()
        if notice is not None:
            notice_uuid = str(notice.uuid)
            notice.delete()
            async_to_sync(channel_layer.group_send)(
                f'notification-{instance.author.uuid}',
                {
                    'type': 'send_json_data',
                    'action': 'deleted',
                    'data': notice_uuid,
                }
            )


@receiver(like_obj, sender=Photo)
def photo_liked(sender, instance, user, **kwargs):
    """ Save and send album liked notification """
    if instance.author.uuid != user.uuid:
        notice = Notification.objects.create(
            initiator=user,
            recipient=instance.author,
            reason=ReasonOfNotification.LIKE_PHOTO,
            content_object=instance,
        )

        notice_data = NotificationShortSerializer(notice).data
        if notice_data['initiator']['avatar']:
            avatar_url = notice_data['initiator']['avatar']
            notice_data['initiator']['avatar'] = f'{settings.API_URL}{avatar_url}'
        
        notice_data['content_object'] = PhotoShortReadSerializer(instance).data
        thumbnail_url = notice_data['content_object']['thumbnail']
        notice_data['content_object']['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

        async_to_sync(channel_layer.group_send)(
            f'notification-{notice.recipient.uuid}',
            {
                'type': 'send_json_data',
                'action': 'created',
                'data': notice_data,
            }
        )


@receiver(dislike_obj, sender=Photo)
def photo_disliked(sender, instance, user, **kwargs):
    """ Delete and send album disliked notification """
    if instance.author.uuid != user.uuid:
        notice = Notification.objects.filter(
            initiator=user,
            recipient=instance.author,
            reason=ReasonOfNotification.LIKE_PHOTO,
            content_type=ContentType.objects.get_for_model(Photo),
            object_uuid=instance.uuid,
        ).first()
        if notice is not None:
            notice_uuid = str(notice.uuid)
            notice.delete()
            async_to_sync(channel_layer.group_send)(
                f'notification-{instance.author.uuid}',
                {
                    'type': 'send_json_data',
                    'action': 'deleted',
                    'data': notice_uuid,
                }
            )


@receiver(post_save, sender=Comment)
def comment_saved(sender, instance, created, **kwargs):
    """ Save and send comment notification """
    if instance.author.uuid != instance.content_object.author.uuid:
        if created:
            notice = Notification.objects.create(
                initiator=instance.author,
                recipient=instance.content_object.author,
                reason=ReasonOfNotification.COMMENT,
                content_object=instance,
            )

            notice_data = NotificationShortSerializer(notice).data
            if notice_data['initiator']['avatar']:
                avatar_url = notice_data['initiator']['avatar']
                notice_data['initiator']['avatar'] = f'{settings.API_URL}{avatar_url}'
            
            notice_data['content_object'] = CommentShortReadSerializer(instance).data
            thumbnail_url = notice_data['content_object']['content_object']['thumbnail']
            notice_data['content_object']['content_object']['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

            async_to_sync(channel_layer.group_send)(
                f'notification-{notice.recipient.uuid}',
                {
                    'type': 'send_json_data',
                    'action': 'created',
                    'data': notice_data,
                }
            )
        else:
            content_object_data = CommentShortReadSerializer(instance).data
            thumbnail_url = content_object_data['content_object']['thumbnail']
            content_object_data['content_object']['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

            notice = Notification.objects.filter(
                initiator=instance.author,
                recipient=instance.content_object.author,
                reason=ReasonOfNotification.COMMENT,
                content_type=ContentType.objects.get_for_model(Comment),
                object_uuid=instance.uuid,
            ).first()

            if notice is not None:
                async_to_sync(channel_layer.group_send)(
                    f'notification-{instance.content_object.author.uuid}',
                    {
                        'type': 'send_json_data',
                        'action': 'updated',
                        'data': {
                            'uuid': str(notice.uuid),
                            'content_object': content_object_data,
                        },
                    }
                )


@receiver(pre_delete, sender=Comment)
def comment_deleting(sender, instance, **kwargs):
    """ Delete and send comment notification """
    if instance.author.uuid != instance.content_object.author.uuid:
        notice = Notification.objects.filter(
            initiator=instance.author,
            recipient=instance.content_object.author,
            reason=ReasonOfNotification.COMMENT,
            content_type=ContentType.objects.get_for_model(Comment),
            object_uuid=instance.uuid,
        ).first()
        if notice is not None:
            notice_uuid = str(notice.uuid)
            notice.delete()
            async_to_sync(channel_layer.group_send)(
                f'notification-{instance.content_object.author.uuid}',
                {
                    'type': 'send_json_data',
                    'action': 'deleted',
                    'data': notice_uuid,
                }
            )


@receiver(post_save, sender=Review)
def review_saved(sender, instance, created, **kwargs):
    """ Save and send review notification """
    if instance.user.uuid != instance.author.uuid:
        if created:
            notice = Notification.objects.create(
                initiator=instance.author,
                recipient=instance.user,
                reason=ReasonOfNotification.REVIEW,
                content_object=instance,
            )

            notice_data = NotificationShortSerializer(notice).data
            if notice_data['initiator']['avatar']:
                avatar_url = notice_data['initiator']['avatar']
                notice_data['initiator']['avatar'] = f'{settings.API_URL}{avatar_url}'
            notice_data['content_object'] = ReviewShortReadSerializer(instance).data

            async_to_sync(channel_layer.group_send)(
                f'notification-{notice.recipient.uuid}',
                {
                    'type': 'send_json_data',
                    'action': 'created',
                    'data': notice_data,
                }
            )
        else:
            content_object_data = ReviewShortReadSerializer(instance).data
            notice = Notification.objects.filter(
                initiator=instance.author,
                recipient=instance.user,
                reason=ReasonOfNotification.REVIEW,
                content_type=ContentType.objects.get_for_model(Review),
                object_uuid=instance.uuid,
            ).first()
            
            if notice is not None:
                async_to_sync(channel_layer.group_send)(
                    f'notification-{notice.recipient.uuid}',
                    {
                        'type': 'send_json_data',
                        'action': 'updated',
                        'data': {
                            'uuid': str(notice.uuid),
                            'content_object': content_object_data,
                        },
                    }
                )


@receiver(pre_delete, sender=Review)
def review_deleting(sender, instance, **kwargs):
    """ Delete and send review notification """
    if instance.user.uuid != instance.author.uuid:
        notice = Notification.objects.filter(
            initiator=instance.author,
            recipient=instance.user,
            reason=ReasonOfNotification.REVIEW,
            content_type=ContentType.objects.get_for_model(Review),
            object_uuid=instance.uuid,
        ).first()

        if notice is not None:
            notice_uuid = str(notice.uuid)
            notice.delete()
            async_to_sync(channel_layer.group_send)(
                f'notification-{instance.user.uuid}',
                {
                    'type': 'send_json_data',
                    'action': 'deleted',
                    'data': notice_uuid,
                }
            )


@receiver(msg_saved, sender=Message)
def message_saved(sender, instance, **kwargs):
    """ Save and send message notification """
    for user in instance.chat.members.exclude(uuid=instance.author.uuid):
        user_connect = caches['connections'].get(str(user.uuid), 0)
        if user_connect <= 0:
            notice = Notification.objects.create(
                initiator=instance.author,
                recipient=user,
                reason=ReasonOfNotification.MESSAGE,
                content_object=instance,
            )

            notice_data = NotificationShortSerializer(notice).data
            if notice_data['initiator']['avatar']:
                avatar_url = notice_data['initiator']['avatar']
                notice_data['initiator']['avatar'] = f'{settings.API_URL}{avatar_url}'
            notice_data['content_object'] = MessageBriefReadSerializer(instance).data

            async_to_sync(channel_layer.group_send)(
                f'notification-{notice.recipient.uuid}',
                {
                    'type': 'send_json_data',
                    'action': 'created',
                    'data': notice_data,
                }
            )
