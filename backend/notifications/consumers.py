from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Notification
from .serializers import NotificationListSerializer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    """ Notification Consumer """

    async def connect(self):
        self.user = self.scope['user']
        self.notification_group_name = f'notification-{self.user.uuid}'

        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.notification_group_name,
                self.channel_name,
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name,
        )

    async def receive_json(self, content):
        notice_uuid = content['notice_uuid']
        notice_viewed = await self.set_notice_viewed(notice_uuid)

        await self.send_json({
            'action': 'viewed',
            'data': {
                'uuid': notice_uuid,
                'viewed': notice_viewed,
            },
        })

    async def send_json_data(self, event):
        await self.send_json({
            'action': event['action'],
            'data': event['data'],
        })

    @database_sync_to_async
    def set_notice_viewed(self, notice_uuid):
        try:
            notice = Notification.objects.get(uuid=notice_uuid)
        except Notification.DoesNotExist:
            return False

        notice.viewed = True
        notice.save(update_fields=['viewed'])
        return notice.viewed
