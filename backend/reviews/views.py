from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from .filters import ReviewFilter
from .models import Review
from .pagination import ReviewPagination
from .permissions import UserIsAuthor
from .serializers import (
    ReviewListCreateSerializer,
    ReviewUpdateDestroySerializer,
)


class ReviewListCreateView(generics.ListCreateAPIView):
    """ Review List Create View """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewListCreateSerializer
    pagination_class = ReviewPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewUpdateDestroyView(
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        generics.GenericAPIView):
    """ Review Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsAuthor]
    queryset = Review.objects.all()
    lookup_field = 'uuid'
    serializer_class = ReviewUpdateDestroySerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
