from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .filters import CityFilter
from .models import Currency, City, Magazine, Tag
from .serializers import (
    CurrencySerializer,
    CitySerializer,
    MagazineSerializer,
    TagSerializer,
)


class CurrencyRetrieveView(generics.RetrieveAPIView):
    """ Currency Retrieve View """
    permission_classes = [AllowAny]
    queryset = Currency.objects.all()
    lookup_field = 'code'
    serializer_class = CurrencySerializer


class CityListView(generics.ListAPIView):
    """ City List View """
    permission_classes = [AllowAny]
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CityFilter


class MagazineView(APIView):
    """ Magazine View """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        obj = Magazine.objects.last()
        serializer = MagazineSerializer(obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagRetrieveView(generics.RetrieveAPIView):
    """ Tag Retrieve View """
    permission_classes = [AllowAny]
    queryset = Tag.objects.all()
    lookup_field = 'uuid'
    serializer_class = TagSerializer
