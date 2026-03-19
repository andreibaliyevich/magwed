from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from accounts.serializers import UserAuthorReadSerializer
from main.serializers import TagSerializer
from .models import Category, Article


class ArticleBriefReadSerializer(serializers.ModelSerializer):
    """ Article Brief Read Serializer """

    class Meta:
        model = Article
        fields = [
            'slug',
            'thumbnail',
        ]


class ArticleShortReadSerializer(serializers.ModelSerializer):
    """ Article Short Read Serializer """

    class Meta:
        model = Article
        fields = [
            'slug',
            'translated_title',
            'thumbnail',
        ]


class ArticleListSerializer(serializers.ModelSerializer):
    """ Article List Serializer """

    class Meta:
        model = Article
        fields = [
            'slug',
            'categories',
            'translated_title',
            'thumbnail',
            'translated_description',
            'published_at',
        ]


class ArticleRetrieveSerializer(serializers.ModelSerializer):
    """ Article Retrieve Serializer """
    author = UserAuthorReadSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    favorite = serializers.SerializerMethodField()

    def get_favorite(self, obj):
        if self.context['request'].user.is_authenticated:
            return self.context['request'].user.favorites.filter(
                content_type=ContentType.objects.get_for_model(obj),
                object_uuid=obj.uuid,
            ).exists()
        return False

    class Meta:
        model = Article
        fields = [
            'uuid',
            'author',
            'categories',
            'translated_title',
            'image',
            'translated_description',
            'translated_content',
            'tags',
            'published_at',
            'view_count',
            'favorite',
        ]
