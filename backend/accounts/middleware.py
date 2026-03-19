from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


class WebSocketAuthMiddleware:
    """ WebSocket Auth Middleware """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        token_key = scope['query_string'].decode()
        scope['user'] = await get_user(token_key)
        return await self.app(scope, receive, send)
