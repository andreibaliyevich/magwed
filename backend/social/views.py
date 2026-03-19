from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from accounts.permissions import UserIsOrganizer
from accounts.serializers import UserBriefReadSerializer
from .filters import FollowFilter, FavoriteFilter
from .models import SocialLink, Follow, Favorite
from .pagination import (
    FollowPagination,
    FavoritePagination,
)
from .serializers import (
    SocialLinkSerializer,
    FollowersSerializer,
    FollowingSerializer,
    FavoriteContentObjectSerializer,
    FavoriteListSerializer,
)


UserModel = get_user_model()


class SocialLinkListCreateView(generics.ListCreateAPIView):
    """ Social Link List Create View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    serializer_class = SocialLinkSerializer

    def get_queryset(self):
        return SocialLink.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SocialLinkUpdateDestroyView(
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        generics.GenericAPIView):
    """ Social Link Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    lookup_field = 'uuid'
    serializer_class = SocialLinkSerializer

    def get_queryset(self):
        return SocialLink.objects.filter(user=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class FollowCreateDestroyView(APIView):
    """ Follow Create Destroy View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(UserModel, uuid=kwargs['uuid'])
        try:
            Follow.objects.create(follower=request.user, user=user)
        except:
            return Response(
                {'detail': _('You have already follow this user.')},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(UserModel, uuid=kwargs['uuid'])
        try:
            Follow.objects.get(follower=request.user, user=user).delete()
        except:
            return Response(
                {'detail': _('You do not follow this user.')},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListView(generics.ListAPIView):
    """ Follow List View """
    permission_classes = [IsAuthenticated]
    queryset = Follow.objects.all()
    pagination_class = FollowPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = FollowFilter

    def get_serializer_class(self):
        if self.request.query_params.get('follower', None):
            return FollowingSerializer
        return FollowersSerializer


class RelatedUserListView(generics.ListAPIView):
    """ Related User List View """
    permission_classes = [IsAuthenticated]
    serializer_class = UserBriefReadSerializer
    pagination_class = FollowPagination

    def get_queryset(self):
        following_uuid = self.request.user.following.values_list(
            'user__uuid',
            flat=True,
        )
        followers_uuid = self.request.user.followers.values_list(
            'follower__uuid',
            flat=True,
        )
        queryset = UserModel.objects.filter(
            Q(uuid__in=following_uuid) | Q(uuid__in=followers_uuid)
        )
        return queryset


class FavoriteCreateDestroyView(APIView):
    """ Favorite Create Destroy View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = FavoriteContentObjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content_object = serializer.content_object

        try:
            Favorite.objects.create(
                user=request.user,
                content_object=content_object,
            )
        except:
            return Response(
                {'detail': _('You already have this favorite.')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        serializer = FavoriteContentObjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content_object = serializer.content_object

        try:
            Favorite.objects.get(
                user=request.user,
                content_type=ContentType.objects.get_for_model(content_object),
                object_uuid=content_object.uuid,
            ).delete()
        except:
            return Response(
                {'detail': _('You do not have this favorite.')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteListView(generics.ListAPIView):
    """ Favorite List View """
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteListSerializer
    pagination_class = FavoritePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = FavoriteFilter

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
