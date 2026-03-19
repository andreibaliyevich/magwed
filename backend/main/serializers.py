from rest_framework import serializers
from django.db.utils import DataError
from django.utils.translation import gettext_lazy as _
from .models import Currency, City, Tag, Magazine


class CurrencySerializer(serializers.ModelSerializer):
    """ Currency Serializer """

    class Meta:
        model = Currency
        fields = ['conversion_rate']


class CitySerializer(serializers.ModelSerializer):
    """ City Serializer """

    class Meta:
        model = City
        fields = ['code']


class MagazineSerializer(serializers.ModelSerializer):
    """ Magazine Serializer """

    class Meta:
        model = Magazine
        fields = [
            'title',
            'slug',
            'image',
            'file',
            'published_at',
        ]


class TagRelatedField(serializers.RelatedField):
    """ Tag Related Field """

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        try:
            obj, created = Tag.objects.get_or_create(name=data)
        except (TypeError, ValueError, DataError):
            raise serializers.ValidationError(_('Invalid data.'))
        return obj.uuid

    def get_queryset(self):
        return Tag.objects.all()


class TagSerializer(serializers.ModelSerializer):
    """ Tag Serializer """

    class Meta:
        model = Tag
        fields = [
            'uuid',
            'name',
        ]
