from django_filters import rest_framework as filters
from .models import Country, City


class CityFilter(filters.FilterSet):
    """ City Filter """
    country = filters.ModelMultipleChoiceFilter(queryset=Country.objects.all())

    class Meta:
        model = City
        fields = ['country']
