from django_filters import rest_framework as filters
from .models import Review


class ReviewFilter(filters.FilterSet):
    """ Review Filter """

    class Meta:
        model = Review
        fields = ['user']
