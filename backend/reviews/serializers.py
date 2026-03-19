from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from accounts.serializers import UserShortReadSerializer
from .models import Review


UserModel = get_user_model()


class ReviewShortReadSerializer(serializers.ModelSerializer):
    """ Review Short Read Serializer """

    class Meta:
        model = Review
        fields = [
            'rating',
            'comment',
        ]


class ReviewListCreateSerializer(serializers.ModelSerializer):
    """ Review List Create Serializer """
    user = serializers.PrimaryKeyRelatedField(
        write_only=True,
        required=False,
        queryset=UserModel.objects.all(),
    )
    author = UserShortReadSerializer(read_only=True)

    def create(self, validated_data):
        try:
            instance = Review.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'create': _('You have already left a review here.')})
        return instance

    class Meta:
        model = Review
        fields = [
            'uuid',
            'user',
            'author',
            'rating',
            'comment',
            'created_at',
        ]


class ReviewUpdateDestroySerializer(serializers.ModelSerializer):
    """ Review Update Destroy Serializer """

    class Meta:
        model = Review
        fields = [
            'uuid',
            'rating',
            'comment',
        ]
