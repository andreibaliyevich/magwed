from contextlib import suppress
from exif import Image as ExifImage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F
from django.shortcuts import get_object_or_404
from accounts.permissions import UserIsOrganizer
from .filters import AlbumFilter, PhotoFilter
from .models import Album, Photo
from .pagination import PortfolioPagination
from .serializers import (
    AlbumListCreateSerializer,
    AlbumImageSerializer,
    AlbumRUDSerializer,
    AlbumListShortSerializer,
    AlbumListSerializer,
    AlbumRetrieveSerializer,
    PhotoListCreateSerializer,
    PhotoRUDSerializer,
    PhotoListShortSerializer,
    PhotoListSerializer,
    PhotoRetrieveSerializer,
)
from .signals import like_obj, dislike_obj


class AlbumListCreateView(generics.ListCreateAPIView):
    """ Album List Create View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    serializer_class = AlbumListCreateSerializer
    pagination_class = PortfolioPagination

    def get_queryset(self):
        return Album.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            thumbnail=self.request.data['image'],
        )


class AlbumImageUpdateView(generics.UpdateAPIView):
    """ Album Image Update View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    lookup_field = 'uuid'
    serializer_class = AlbumImageSerializer

    def get_queryset(self):
        return Album.objects.filter(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(thumbnail=self.request.data['image'])


class AlbumRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Album Retrieve Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    lookup_field = 'uuid'
    serializer_class = AlbumRUDSerializer

    def get_queryset(self):
        return Album.objects.filter(author=self.request.user)


class AlbumListView(generics.ListAPIView):
    """ Album List View """
    permission_classes = [AllowAny]
    queryset = Album.objects.all()
    pagination_class = PortfolioPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = AlbumFilter
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.request.query_params.get('author', None):
            return AlbumListShortSerializer
        return AlbumListSerializer


class AlbumRetrieveView(generics.RetrieveAPIView):
    """ Album Retrieve View """
    permission_classes = [AllowAny]
    queryset = Album.objects.all()
    lookup_field = 'uuid'
    serializer_class = AlbumRetrieveSerializer


class AlbumUpViewCountView(APIView):
    """ Album Up View Count View """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        Album.objects.filter(
            uuid=kwargs['uuid']).update(
            view_count=F('view_count') + 1)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AlbumLikeView(APIView):
    """ Album Like View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Album, uuid=kwargs['uuid'])
        try:
            obj.likes.add(request.user)
        except:
            return Response(
                {'detail': _('You already liked this album!')},
                status=status.HTTP_400_BAD_REQUEST,
            )
        like_obj.send(sender=Album, instance=obj, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(Album, uuid=kwargs['uuid'])
        try:
            obj.likes.remove(request.user)
        except:
            return Response(
                {'detail': _('You do not like this album!')},
                status=status.HTTP_400_BAD_REQUEST,
            )
        dislike_obj.send(sender=Album, instance=obj, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoListCreateView(generics.ListCreateAPIView):
    """ Photo List Create View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    serializer_class = PhotoListCreateSerializer
    pagination_class = PortfolioPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PhotoFilter

    def get_queryset(self):
        return Photo.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        extra_data = {
            'author': self.request.user,
            'thumbnail': self.request.data['image'],
        }

        exif_img = ExifImage(self.request.data['image'])
        with suppress(Exception):
            extra_data['device'] = f'{exif_img.make} {exif_img.model}'
        with suppress(Exception):
            extra_data['f_number'] = exif_img.f_number
        with suppress(Exception):
            extra_data['exposure_time'] = f'''1/{
                int(1 / float(exif_img.exposure_time))
            }'''
        with suppress(Exception):
            extra_data['focal_length'] = exif_img.focal_length
        with suppress(Exception):
            extra_data['photographic_sensitivity'] = f'''{
                exif_img.photographic_sensitivity
            }'''

        serializer.save(**extra_data)


class PhotoRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Photo Retrieve Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    lookup_field = 'uuid'
    serializer_class = PhotoRUDSerializer

    def get_queryset(self):
        return Photo.objects.filter(author=self.request.user)


class PhotoListView(generics.ListAPIView):
    """ Photo List View """
    permission_classes = [AllowAny]
    queryset = Photo.objects.all()
    pagination_class = PortfolioPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = PhotoFilter
    ordering_fields = ['uploaded_at', 'rating']
    ordering = ['-uploaded_at']
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if (self.request.query_params.get('author', None)
                or self.request.query_params.get('album', None)):
            return PhotoListShortSerializer
        return PhotoListSerializer


class PhotoRetrieveView(generics.RetrieveAPIView):
    """ Photo Retrieve View """
    permission_classes = [AllowAny]
    queryset = Photo.objects.all()
    lookup_field = 'uuid'
    serializer_class = PhotoRetrieveSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_class = PhotoFilter
    ordering_fields = ['uploaded_at', 'rating']
    ordering = ['-uploaded_at']

    def get_prev_and_next(self, queryset, obj):
        uuid_list = list(queryset.values_list('uuid', flat=True))
        uuid_index = uuid_list.index(obj.uuid)

        if uuid_index == 0:
            prev_photo_uuid = None
            next_photo_uuid = uuid_list[uuid_index + 1]
        elif uuid_index == len(uuid_list) - 1:
            prev_photo_uuid = uuid_list[uuid_index - 1]
            next_photo_uuid = None
        else:
            prev_photo_uuid = uuid_list[uuid_index - 1]
            next_photo_uuid = uuid_list[uuid_index + 1]

        data = {
            'prev_photo_uuid': prev_photo_uuid,
            'next_photo_uuid': next_photo_uuid,
        }
        return data

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, uuid=kwargs[self.lookup_field])
        self.check_object_permissions(self.request, obj)
        serializer = self.get_serializer(obj)
        data = serializer.data
        data.update(self.get_prev_and_next(queryset, obj))
        return Response(data, status=status.HTTP_200_OK)


class PhotoUpViewCountView(APIView):
    """ Photo Up View Count View """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        Photo.objects.filter(
            uuid=kwargs['uuid']).update(
            view_count=F('view_count') + 1)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoLikeView(APIView):
    """ Photo Like View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Photo, uuid=kwargs['uuid'])
        try:
            obj.likes.add(request.user)
        except:
            return Response(
                {'detail': _('You already liked this photo!')},
                status=status.HTTP_400_BAD_REQUEST,
            )
        like_obj.send(sender=Photo, instance=obj, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(Photo, uuid=kwargs['uuid'])
        try:
            obj.likes.remove(request.user)
        except:
            return Response(
                {'detail': _('You do not like this photo!')},
                status=status.HTTP_400_BAD_REQUEST,
            )
        dislike_obj.send(sender=Photo, instance=obj, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
