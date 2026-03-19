from django_filters import rest_framework as filters
from .models import Organizer


class OrganizerFilter(filters.FilterSet):
    """ Organizer Filter """
    cost_work = filters.RangeFilter()

    class Meta:
        model = Organizer
        fields = [
            'roles',
            'countries',
            'cities',
            'languages',
            'cost_work',
        ]
