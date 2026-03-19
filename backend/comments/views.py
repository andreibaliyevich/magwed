from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from .filters import CommentFilter
from .models import Comment
from .pagination import CommentPagination
from .permissions import UserIsAuthor
from .serializers import (
    CommentListCreateSerializer,
    CommentUpdateDestroySerializer,
)


channel_layer = get_channel_layer()


class CommentListCreateView(generics.ListCreateAPIView):
    """ Comment List Create View """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentListCreateSerializer
    pagination_class = CommentPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter

    def get_comment_uuid(self, instance):
        if instance.content_type.model == 'comment':
            return str(instance.object_uuid)
        return None

    def get_content_type_object_uuid(self, instance):
        if instance.content_type.model == 'comment':
            return self.get_content_type_object_uuid(instance.content_object)
        return (instance.content_type.model, instance.object_uuid)

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)

        content_type, object_uuid = self.get_content_type_object_uuid(instance)
        async_to_sync(channel_layer.group_send)(
            f'comment-{content_type}-{object_uuid}',
            {
                'type': 'send_json_data',
                'action': 'create',
                'data': {
                    'comment_uuid': self.get_comment_uuid(instance),
                    'instance': serializer.data,
                },
            }
        )

        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)


class CommentUpdateDestroyView(
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        generics.GenericAPIView):
    """ Comment Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsAuthor]
    queryset = Comment.objects.all()
    lookup_field = 'uuid'
    serializer_class = CommentUpdateDestroySerializer

    def get_content_type_object_uuid(self, instance):
        if instance.content_type.model == 'comment':
            return self.get_content_type_object_uuid(instance.content_object)
        return (instance.content_type.model, instance.object_uuid)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        content_type, object_uuid = self.get_content_type_object_uuid(instance)
        async_to_sync(channel_layer.group_send)(
            f'comment-{content_type}-{object_uuid}',
            {
                'type': 'send_json_data',
                'action': 'update',
                'data': serializer.data,
            }
        )

        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_uuid = instance.uuid
        content_type, object_uuid = self.get_content_type_object_uuid(instance)
        self.perform_destroy(instance)

        async_to_sync(channel_layer.group_send)(
            f'comment-{content_type}-{object_uuid}',
            {
                'type': 'send_json_data',
                'action': 'destroy',
                'data': str(instance_uuid),
            }
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
