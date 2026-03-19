from django.urls import path, include
from . import views


urlpatterns = [
    path('chat/', include([
        path('list/', views.ChatListView.as_view()),
        path('create/', views.ChatCreateView.as_view()),
        path('retrieve/<uuid:uuid>/', views.ChatRetrieveView.as_view()),
        path('group-retrieve/<uuid:uuid>/',
            views.GroupChatRetrieveView.as_view()),
        path('destroy/<uuid:uuid>/', views.ChatDestroyView.as_view()),
        path('leave/<uuid:uuid>/', views.ChatLeaveView.as_view()),
    ])),
    path('message/', include([
        path('list/', views.MessageListView.as_view()),
        path('new/<uuid:chat_uuid>/<int:msg_type>/',
            views.NewMessageView.as_view()),
        path('write/<uuid:user_uuid>/', views.WriteMessageView.as_view()),
    ])),
]
