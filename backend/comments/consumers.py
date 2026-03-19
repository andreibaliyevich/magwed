from channels.generic.websocket import AsyncJsonWebsocketConsumer


class CommentConsumer(AsyncJsonWebsocketConsumer):
    """ Comment Consumer """

    async def connect(self):
        self.comment_group_name = f'''comment-{
            self.scope['url_route']['kwargs']['content_type']
        }-{
            self.scope['url_route']['kwargs']['object_uuid']
        }'''

        await self.channel_layer.group_add(
            self.comment_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.comment_group_name,
            self.channel_name,
        )

    async def send_json_data(self, event):
        await self.send_json({
            'action': event['action'],
            'data': event['data'],
        })
