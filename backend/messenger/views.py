from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from .choices import ChatType, MessageType
from .filters import MessageFilter
from .models import Chat, Message
from .pagination import ChatPagination, MessagePagination
from .permissions import ChatIsGroupChat, ChatDestroyPermission
from .serializers import (
    ChatListSerializer,
    ChatCreateSerializer,
    GroupChatSerializer,
    ChatRetrieveSerializer,
    GroupChatRetrieveSerializer,
    TextMessageSerializer,
    ImageMessageSerializer,
    FileMessageSerializer,
    MessageShortReadSerializer,
    MessageFullReadSerializer,
)
from .signals import msg_saved


UserModel = get_user_model()
channel_layer = get_channel_layer()


class ChatListView(generics.ListAPIView):
    """ Chat List View """
    permission_classes = [IsAuthenticated]
    serializer_class = ChatListSerializer
    pagination_class = ChatPagination

    def get_queryset(self):
        return Chat.objects.filter(members=self.request.user)


class ChatCreateView(APIView):
    """ Chat Create View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        chat_serializer = ChatCreateSerializer(data=request.data)
        chat_serializer.is_valid(raise_exception=True)
        chat_valid_data = chat_serializer.validated_data
        chat = None

        if chat_valid_data['chat_type'] == ChatType.DIALOG:
            dialog_chats = Chat.objects.filter(
                chat_type=ChatType.DIALOG,
                members=request.user,
            )
            for dialog in dialog_chats:
                if chat_valid_data['members'][0] == dialog.members.exclude(
                        uuid=request.user.uuid).first():
                    chat = dialog
                    break
            if chat is None:
                chat = chat_serializer.save()
                chat.members.add(request.user)
            else:
                return Response(
                    {'uuid': chat.uuid},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        elif chat_valid_data['chat_type'] == ChatType.GROUP:
            group_chat_serializer = GroupChatSerializer(data=request.data)
            group_chat_serializer.is_valid(raise_exception=True)

            chat = chat_serializer.save()
            chat.members.add(request.user)
            group_chat_serializer.save(chat=chat, owner=request.user)

        for member in chat.members.all():
            chat_data = ChatListSerializer(
                chat,
                context={
                    'request': request,
                    'user': member,
                },
            ).data
            async_to_sync(channel_layer.group_send)(
                f'chat-list-{member.uuid}',
                {
                    'type': 'send_json_data',
                    'action': 'create_chat',
                    'data': chat_data,
                }
            )
        return Response(status=status.HTTP_201_CREATED)


class ChatRetrieveView(generics.RetrieveAPIView):
    """ Chat Retrieve View """
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'
    serializer_class = ChatRetrieveSerializer

    def get_queryset(self):
        return Chat.objects.filter(members=self.request.user)


class GroupChatRetrieveView(generics.RetrieveAPIView):
    """ Group Chat Retrieve View """
    permission_classes = [IsAuthenticated, ChatIsGroupChat]
    lookup_field = 'uuid'
    serializer_class = GroupChatRetrieveSerializer

    def get_queryset(self):
        return Chat.objects.filter(members=self.request.user)


class ChatDestroyView(generics.DestroyAPIView):
    """ Chat Destroy View """
    permission_classes = [IsAuthenticated, ChatDestroyPermission]
    lookup_field = 'uuid'

    def get_queryset(self):
        return Chat.objects.filter(members=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_uuid = instance.uuid
        uuid_list = list(instance.members.values_list('uuid', flat=True))
        self.perform_destroy(instance)

        for member_uuid in uuid_list:
            async_to_sync(channel_layer.group_send)(
                f'chat-list-{member_uuid}',
                {
                    'type': 'send_json_data',
                    'action': 'destroy_chat',
                    'data': str(instance_uuid),
                }
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChatLeaveView(APIView):
    """ Chat Leave View """
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        queryset = Chat.objects.filter(members=request.user)
        obj = get_object_or_404(queryset, uuid=kwargs['uuid'])
        obj.members.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageListView(generics.ListAPIView):
    """ Message List View """
    permission_classes = [IsAuthenticated]
    serializer_class = MessageFullReadSerializer
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        return Message.objects.filter(chat__members=self.request.user)


class NewMessageView(APIView):
    """ New Message View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        chats = Chat.objects.filter(members=request.user)
        chat = get_object_or_404(chats, uuid=kwargs['chat_uuid'])

        if kwargs['msg_type'] == MessageType.TEXT:
            text_serializer = TextMessageSerializer(data=request.data)
            text_serializer.is_valid(raise_exception=True)
            msg = Message.objects.create(
                chat=chat,
                author=request.user,
                msg_type=MessageType.TEXT,
            )
            text_serializer.save(message=msg)
        elif kwargs['msg_type'] == MessageType.IMAGES:
            msg = Message.objects.create(
                chat=chat,
                author=request.user,
                msg_type=MessageType.IMAGES,
            )
            images = request.data.getlist('content', [])
            for img in images:
                img_serializer = ImageMessageSerializer(data={'content': img})
                img_serializer.is_valid(raise_exception=True)
                img_serializer.save(message=msg)
        elif kwargs['msg_type'] == MessageType.FILES:
            msg = Message.objects.create(
                chat=chat,
                author=request.user,
                msg_type=MessageType.FILES,
            )
            files = request.data.getlist('content', [])
            for file in files:
                file_serializer = FileMessageSerializer(data={'content': file})
                file_serializer.is_valid(raise_exception=True)
                file_serializer.save(message=msg)
        else:
            return Response(
                {'detail': _('Not found.')},
                status=status.HTTP_404_NOT_FOUND
            )

        chat.last_message = msg
        chat.save(update_fields=['last_message'])

        msg_short_data = MessageShortReadSerializer(
            msg,
            context={'request': request},
        ).data
        msg_full_data = MessageFullReadSerializer(
            msg,
            context={'request': request},
        ).data

        for member in chat.members.all():
            async_to_sync(channel_layer.group_send)(
                f'chat-list-{member.uuid}',
                {
                    'type': 'send_json_data',
                    'action': 'new_msg',
                    'data': {
                        'chat_uuid': str(chat.uuid),
                        'author_uuid': str(msg.author.uuid),
                        'msg': msg_short_data,
                    },
                }
            )
        async_to_sync(channel_layer.group_send)(
            f'chat-{chat.uuid}',
            {
                'type': 'send_json_data',
                'action': 'new_msg',
                'data': msg_full_data,
            }
        )
        msg_saved.send(sender=Message, instance=msg)
        return Response(status=status.HTTP_201_CREATED)


class WriteMessageView(APIView):
    """ Write Message View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(UserModel, uuid=kwargs['user_uuid'])

        text_serializer = TextMessageSerializer(data=request.data)
        text_serializer.is_valid(raise_exception=True)

        chat = None
        chat_created = False
        dialog_chats = Chat.objects.filter(
            chat_type=ChatType.DIALOG,
            members=request.user,
        )

        for dialog in dialog_chats:
            if user == dialog.members.exclude(uuid=request.user.uuid).first():
                chat = dialog
                break
        if chat is None:
            chat = Chat.objects.create(chat_type=ChatType.DIALOG)
            chat.members.add(request.user, user)
            chat_created = True

        msg = Message.objects.create(
            chat=chat,
            author=request.user,
            msg_type=MessageType.TEXT,
        )
        text_serializer.save(message=msg)

        chat.last_message = msg
        chat.save(update_fields=['last_message'])

        if chat_created:
            for member in chat.members.all():
                chat_data = ChatListSerializer(
                    chat,
                    context={
                        'request': request,
                        'user': member,
                    },
                ).data
                async_to_sync(channel_layer.group_send)(
                    f'chat-list-{member.uuid}',
                    {
                        'type': 'send_json_data',
                        'action': 'create_chat',
                        'data': chat_data,
                    }
                )
        else:
            msg_short_data = MessageShortReadSerializer(
                msg,
                context={'request': request},
            ).data
            for member in chat.members.all():
                async_to_sync(channel_layer.group_send)(
                    f'chat-list-{member.uuid}',
                    {
                        'type': 'send_json_data',
                        'action': 'new_msg',
                        'data': {
                            'chat_uuid': str(chat.uuid),
                            'author_uuid': str(msg.author.uuid),
                            'msg': msg_short_data,
                        },
                    }
                )

        msg_full_data = MessageFullReadSerializer(
            msg,
            context={'request': request},
        ).data
        async_to_sync(channel_layer.group_send)(
            f'chat-{chat.uuid}',
            {
                'type': 'send_json_data',
                'action': 'new_msg',
                'data': msg_full_data,
            }
        )

        msg_saved.send(sender=Message, instance=msg)
        return Response(status=status.HTTP_201_CREATED)
