from django_filters import rest_framework as filters
from .models import Article


class ArticleFilter(filters.FilterSet):
    """ Article Filter """
    published_at_year = filters.NumberFilter(
        field_name='published_at',
        lookup_expr='year',
    )

    class Meta:
        model = Article
        fields = [
            'author',
            'categories',
            'tags',
            'published_at_year',
        ]
