from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from main.serializers import TagRelatedField, TagSerializer
from accounts.serializers import UserOwnerReadSerializer
from .models import Album, Photo


class AlbumShortReadSerializer(serializers.ModelSerializer):
    """ Album Short Read Serializer """
    
    class Meta:
        model = Album
        fields = [
            'uuid',
            'thumbnail',
            'title',
        ]


class PhotoShortReadSerializer(serializers.ModelSerializer):
    """ Photo Short Read Serializer """

    class Meta:
        model = Photo
        fields = [
            'uuid',
            'thumbnail',
            'title',
        ]


class PhotoListCreateSerializer(serializers.ModelSerializer):
    """ Photo List Create Serializer """
    album = serializers.PrimaryKeyRelatedField(
        write_only=True,
        required=False,
        queryset=Album.objects.all(),
    )
    image = serializers.ImageField(write_only=True)
    thumbnail = serializers.ImageField(read_only=True)
    title = serializers.CharField(read_only=True)
    uploaded_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Photo
        fields = [
            'uuid',
            'album',
            'image',
            'thumbnail',
            'title',
            'uploaded_at',
        ]


class PhotoRUDSerializer(serializers.ModelSerializer):
    """ Photo Retrieve Update Destroy Serializer """
    image = serializers.ImageField(read_only=True)
    tags = TagRelatedField(many=True)
    uploaded_at = serializers.DateTimeField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    like_count = serializers.SerializerMethodField()
    rating = serializers.FloatField(read_only=True)

    def get_like_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Photo
        fields = [
            'image',
            'device',
            'f_number',
            'exposure_time',
            'focal_length',
            'photographic_sensitivity',
            'title',
            'description',
            'tags',
            'uploaded_at',
            'view_count',
            'like_count',
            'rating',
        ]


class PhotoListShortSerializer(serializers.ModelSerializer):
    """ Photo List Short Serializer """
    like_count = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Photo
        fields = [
            'uuid',
            'thumbnail',
            'title',
            'view_count',
            'like_count',
            'rating',
        ]


class PhotoListSerializer(serializers.ModelSerializer):
    """ Photo List Serializer """
    author = UserOwnerReadSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Photo
        fields = [
            'uuid',
            'author',
            'thumbnail',
            'title',
            'view_count',
            'like_count',
            'rating',
        ]


class PhotoRetrieveSerializer(serializers.ModelSerializer):
    """ Photo Retrieve Serializer """
    author = UserOwnerReadSerializer(read_only=True)
    album = AlbumShortReadSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    like_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_liked(self, obj):
        if self.context['request'].user.is_authenticated:
            return self.context['request'].user in obj.likes.all()
        return False

    def get_favorite(self, obj):
        if self.context['request'].user.is_authenticated:
            return self.context['request'].user.favorites.filter(
                content_type=ContentType.objects.get_for_model(obj),
                object_uuid=obj.uuid,
            ).exists()
        return False

    class Meta:
        model = Photo
        fields = [
            'author',
            'album',
            'image',
            'device',
            'f_number',
            'exposure_time',
            'focal_length',
            'photographic_sensitivity',
            'title',
            'description',
            'tags',
            'uploaded_at',
            'view_count',
            'like_count',
            'liked',
            'rating',
            'favorite',
        ]


class AlbumListCreateSerializer(serializers.ModelSerializer):
    """ Album List Create Serializer """
    image = serializers.ImageField(write_only=True)
    thumbnail = serializers.ImageField(read_only=True)
    description = serializers.CharField(write_only=True, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Album
        fields = [
            'uuid',
            'image',
            'thumbnail',
            'title',
            'description',
            'created_at',
        ]


class AlbumImageSerializer(serializers.ModelSerializer):
    """ Album Image Serializer """

    class Meta:
        model = Album
        fields = ['image']


class AlbumRUDSerializer(serializers.ModelSerializer):
    """ Album Retrieve Update Destroy Serializer """
    image = serializers.ImageField(read_only=True)
    tags = TagRelatedField(many=True)
    created_at = serializers.DateTimeField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    like_count = serializers.SerializerMethodField()
    rating = serializers.FloatField(read_only=True)

    def get_like_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Album
        fields = [
            'image',
            'title',
            'description',
            'tags',
            'created_at',
            'view_count',
            'like_count',
            'rating',
        ]


class AlbumListShortSerializer(serializers.ModelSerializer):
    """ Album List Short Serializer """
    like_count = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Album
        fields = [
            'uuid',
            'thumbnail',
            'title',
            'view_count',
            'like_count',
            'rating',
        ]


class AlbumListSerializer(serializers.ModelSerializer):
    """ Album List Serializer """
    author = UserOwnerReadSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Album
        fields = [
            'uuid',
            'author',
            'thumbnail',
            'title',
            'view_count',
            'like_count',
            'rating',
        ]


class AlbumRetrieveSerializer(serializers.ModelSerializer):
    """ Album Retrieve Serializer """
    author = UserOwnerReadSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    like_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_liked(self, obj):
        if self.context['request'].user.is_authenticated:
            return self.context['request'].user in obj.likes.all()
        return False

    def get_favorite(self, obj):
        if self.context['request'].user.is_authenticated:
            return self.context['request'].user.favorites.filter(
                content_type=ContentType.objects.get_for_model(obj),
                object_uuid=obj.uuid,
            ).exists()
        return False

    class Meta:
        model = Album
        fields = [
            'author',
            'image',
            'title',
            'description',
            'tags',
            'created_at',
            'view_count',
            'like_count',
            'liked',
            'rating',
            'favorite',
        ]
