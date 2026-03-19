from django_filters import rest_framework as filters
from .models import Message


class MessageFilter(filters.FilterSet):
    """ Message Filter """

    class Meta:
        model = Message
        fields = ['chat']
