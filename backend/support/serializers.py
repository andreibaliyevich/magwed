from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from blog.models import Article
from comments.models import Comment
from portfolio.models import Album, Photo
from reviews.models import Review
from .models import Feedback, Report


class FeedbackSerializer(serializers.ModelSerializer):
    """ Feedback Serializer """

    class Meta:
        model = Feedback
        fields = [
            'subject',
            'email',
            'comment',
        ]


class ReportSerializer(serializers.ModelSerializer):
    """ Report Serializer """
    content_type = serializers.CharField(write_only=True)
    object_uuid = serializers.UUIDField(write_only=True)

    def validate(self, data):
        if data['content_type'] == 'user':
            object_class = get_user_model()
        elif data['content_type'] == 'review':
            object_class = Review
        elif data['content_type'] == 'article':
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
            report = Report.objects.create(
                sender=self.context['request'].user,
                content_object=self.content_object,
                comment=validated_data['comment'],
            )
        except BaseException:
            raise serializers.ValidationError({
                'create': _('Failed to create report.')})
        return report

    class Meta:
        model = Report
        fields = [
            'content_type',
            'object_uuid',
            'comment',
        ]
