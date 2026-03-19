from rest_framework.pagination import CursorPagination, PageNumberPagination


class ChatPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class MessagePagination(CursorPagination):
    page_size = 50
    ordering = '-created_at'
