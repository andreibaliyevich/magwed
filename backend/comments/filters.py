from django_filters import rest_framework as filters
from .models import Comment


class CommentFilter(filters.FilterSet):
    """ Comment Filter """

    class Meta:
        model = Comment
        fields = [
            'content_type__model',
            'object_uuid',
        ]
