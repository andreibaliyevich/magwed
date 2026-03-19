from rest_framework import serializers
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from accounts.serializers import (
    UserBriefReadSerializer,
    UserShortReadSerializer,
)
from .choices import ChatType, MessageType
from .models import (
    Chat,
    GroupChat,
    Message,
    TextMessage,
    ImageMessage,
    FileMessage,
)


class TextMessageSerializer(serializers.ModelSerializer):
    """ Text Message Serializer """

    class Meta:
        model = TextMessage
        fields = ['content']


class ImageMessageSerializer(serializers.ModelSerializer):
    """ Image Message Serializer """
    size = serializers.SerializerMethodField()

    def get_size(self, obj):
        return obj.content.size

    class Meta:
        model = ImageMessage
        fields = [
            'uuid',
            'content',
            'size',
        ]


class FileMessageSerializer(serializers.ModelSerializer):
    """ File Message Serializer """
    size = serializers.SerializerMethodField()

    def get_size(self, obj):
        return obj.content.size

    class Meta:
        model = FileMessage
        fields = [
            'uuid',
            'content',
            'size',
        ]


class MessageBriefReadSerializer(serializers.ModelSerializer):
    """ Message Brief Read Serializer """
    chat = serializers.PrimaryKeyRelatedField(
        read_only=True,
        pk_field=serializers.UUIDField(format='hex_verbose'),
    )
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        if obj.msg_type == MessageType.TEXT and hasattr(obj, 'text'):
            return TextMessageSerializer(obj.text).data['content']

        if obj.msg_type == MessageType.IMAGES:
            return obj.images.all().count()

        if obj.msg_type == MessageType.FILES:
            return obj.files.all().count()

        return None

    class Meta:
        model = Message
        fields = [
            'chat',
            'msg_type',
            'content',
        ]


class MessageShortReadSerializer(serializers.ModelSerializer):
    """ Message Short Read Serializer """
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        if obj.msg_type == MessageType.TEXT and hasattr(obj, 'text'):
            return TextMessageSerializer(obj.text).data['content']

        if obj.msg_type == MessageType.IMAGES:
            return obj.images.all().count()

        if obj.msg_type == MessageType.FILES:
            return obj.files.all().count()

        return None

    class Meta:
        model = Message
        fields = [
            'msg_type',
            'created_at',
            'content',
        ]


class MessageFullReadSerializer(serializers.ModelSerializer):
    """ Message Full Read Serializer """
    author = UserBriefReadSerializer(read_only=True)
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        if obj.msg_type == MessageType.TEXT and hasattr(obj, 'text'):
            return TextMessageSerializer(obj.text).data['content']

        if obj.msg_type == MessageType.IMAGES:
            return ImageMessageSerializer(
                obj.images.all(),
                many=True,
                context=self.context,
            ).data

        if obj.msg_type == MessageType.FILES:
            return FileMessageSerializer(
                obj.files.all(),
                many=True,
                context=self.context,
            ).data

        return None

    class Meta:
        model = Message
        fields = [
            'uuid',
            'author',
            'msg_type',
            'created_at',
            'viewed_by',
            'content',
        ]


class GroupChatSerializer(serializers.ModelSerializer):
    """ Group Chat Serializer """
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
        pk_field=serializers.UUIDField(format='hex_verbose'),
    )

    class Meta:
        model = GroupChat
        fields = [
            'owner',
            'name',
            'image',
        ]


class ChatListSerializer(serializers.ModelSerializer):
    """ Chat List Serializer """
    details = serializers.SerializerMethodField()
    last_message = MessageShortReadSerializer(read_only=True)
    unviewed_msg_count = serializers.SerializerMethodField()

    def get_details(self, obj):
        user = self.context.get('user', self.context['request'].user)

        if obj.chat_type == ChatType.DIALOG:
            return UserBriefReadSerializer(
                obj.members.exclude(uuid=user.uuid).first(),
                context=self.context,
            ).data

        if obj.chat_type == ChatType.GROUP:
            return GroupChatSerializer(
                obj.group_details,
                context=self.context,
            ).data

        return None

    def get_unviewed_msg_count(self, obj):
        user = self.context.get('user', self.context['request'].user)
        return obj.messages.exclude(
            author=user).filter(
            ~Q(viewed_by=user)).count()

    class Meta:
        model = Chat
        fields = [
            'uuid',
            'chat_type',
            'details',
            'last_message',
            'unviewed_msg_count',
        ]


class ChatCreateSerializer(serializers.ModelSerializer):
    """ Chat Create Serializer """

    class Meta:
        model = Chat
        fields = [
            'chat_type',
            'members',
        ]


class ChatRetrieveSerializer(serializers.ModelSerializer):
    """ Chat Retrieve Serializer """
    details = serializers.SerializerMethodField()

    def get_details(self, obj):
        request = self.context['request']

        if obj.chat_type == ChatType.DIALOG:
            return UserShortReadSerializer(
                obj.members.exclude(uuid=request.user.uuid).first(),
                context={'request': request},
            ).data

        if obj.chat_type == ChatType.GROUP:
            group_data = GroupChatSerializer(
                obj.group_details,
                context={'request': request},
            ).data
            group_data['member_count'] = obj.members.all().count()
            return group_data

        return None

    class Meta:
        model = Chat
        fields = [
            'uuid',
            'chat_type',
            'details',
        ]


class GroupChatRetrieveSerializer(serializers.ModelSerializer):
    """ Group Chat Retrieve Serializer """
    members = UserShortReadSerializer(read_only=True, many=True)
    group_details = GroupChatSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = [
            'uuid',
            'members',
            'group_details',
        ]
