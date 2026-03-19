from rest_framework import serializers
from accounts.serializers import UserShortReadSerializer
from blog.models import Article
from blog.serializers import ArticleBriefReadSerializer
from comments.models import Comment
from comments.serializers import CommentShortReadSerializer
from messenger.models import Message
from messenger.serializers import MessageBriefReadSerializer
from portfolio.models import Album, Photo
from portfolio.serializers import (
    AlbumShortReadSerializer,
    PhotoShortReadSerializer,
)
from reviews.models import Review
from reviews.serializers import ReviewShortReadSerializer
from social.models import Follow
from .models import Notification


class NotificationShortSerializer(serializers.ModelSerializer):
    """ Notification Short Serializer """
    initiator = UserShortReadSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'uuid',
            'initiator',
            'reason',
            'created_at',
            'viewed',
        ]


class NotificationObjectRelatedField(serializers.RelatedField):
    """
    A notification field to use for the 'content_object' generic relationship.
    """

    def to_representation(self, value):
        if isinstance(value, Follow):
            return None
        elif isinstance(value, Article):
            serializer = ArticleBriefReadSerializer(
                value,
                context=self.context,
            )
        elif isinstance(value, Album):
            serializer = AlbumShortReadSerializer(
                value,
                context=self.context,
            )
        elif isinstance(value, Photo):
            serializer = PhotoShortReadSerializer(
                value,
                context=self.context,
            )
        elif isinstance(value, Comment):
            serializer = CommentShortReadSerializer(
                value,
                context=self.context,
            )
        elif isinstance(value, Review):
            serializer = ReviewShortReadSerializer(
                value,
                context=self.context,
            )
        elif isinstance(value, Message):
            serializer = MessageBriefReadSerializer(
                value,
                context=self.context,
            )
        else:
            raise Exception('Unexpected type of content object')
        return serializer.data


class NotificationListSerializer(serializers.ModelSerializer):
    """ Notification List Serializer """
    initiator = UserShortReadSerializer(read_only=True)
    content_object = NotificationObjectRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'uuid',
            'initiator',
            'reason',
            'content_object',
            'created_at',
            'viewed',
        ]
