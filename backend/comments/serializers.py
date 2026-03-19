from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from accounts.serializers import UserShortReadSerializer
from blog.models import Article
from blog.serializers import ArticleBriefReadSerializer
from portfolio.models import Album, Photo
from portfolio.serializers import (
    AlbumShortReadSerializer,
    PhotoShortReadSerializer,
)
from .models import Comment


class CommentObjectRelatedField(serializers.RelatedField):
    """
    A comment field to use for the 'content_object' generic relationship.
    """

    def to_representation(self, value):
        if isinstance(value, Article):
            serializer_data = ArticleBriefReadSerializer(
                value,
                context=self.context,
            ).data
        elif isinstance(value, Album):
            serializer_data = AlbumShortReadSerializer(
                value,
                context=self.context,
            ).data
        elif isinstance(value, Photo):
            serializer_data = PhotoShortReadSerializer(
                value,
                context=self.context,
            ).data
        elif isinstance(value, Comment):
            return self.to_representation(value.content_object)
        else:
            raise Exception('Unexpected type of content object')
        serializer_data['model_name'] = value._meta.model_name
        return serializer_data


class CommentShortReadSerializer(serializers.ModelSerializer):
    """ Comment Short Read Serializer """
    content_type_model = serializers.SerializerMethodField()
    content_object = CommentObjectRelatedField(read_only=True)

    def get_content_type_model(self, obj):
        return obj.content_type.model

    class Meta:
        model = Comment
        fields = [
            'content_type_model',
            'content_object',
            'content',
        ]


class CommentListCreateSerializer(serializers.ModelSerializer):
    """ Comment List Create Serializer """
    content_type = serializers.CharField(write_only=True)
    object_uuid = serializers.UUIDField(write_only=True)
    author = UserShortReadSerializer(read_only=True)

    def get_fields(self):
        fields = super().get_fields()
        fields['comments'] = CommentListCreateSerializer(
            read_only=True,
            many=True,
        )
        return fields

    def validate(self, data):
        if data['content_type'] == 'article':
            object_class = Article
        elif data['content_type'] == 'album':
            object_class = Album
        elif data['content_type'] == 'photo':
            object_class = Photo
        elif data['content_type'] == 'comment':
            object_class = Comment
        else:
            raise serializers.ValidationError({
                'content_type': _('Invalid content type.')})

        try:
            self.content_object = object_class.objects.get(
                uuid=data['object_uuid'])
        except object_class.DoesNotExist:
            raise serializers.ValidationError({
                'object_uuid': _('Object does not exist.')})

        return data

    def create(self, validated_data):
        try:
            comment = Comment.objects.create(
                author=self.context['request'].user,
                content_object=self.content_object,
                content=validated_data['content'],
            )
        except BaseException:
            raise serializers.ValidationError({
                'create': _('Failed to create comment.')})
        return comment

    class Meta:
        model = Comment
        fields = [
            'uuid',
            'content_type',
            'object_uuid',
            'author',
            'content',
            'created_at',
            'comments',
        ]


class CommentUpdateDestroySerializer(serializers.ModelSerializer):
    """ Comment Update Destroy Serializer """

    class Meta:
        model = Comment
        fields = [
            'uuid',
            'content',
        ]
