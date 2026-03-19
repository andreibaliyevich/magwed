from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'^ws/comments/'
            r'(?P<content_type>[a-z]+)/'
            r'(?P<object_uuid>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
        consumers.CommentConsumer.as_asgi(),
    ),
]
