from django.urls import path
from . import views


urlpatterns = [
    path('', views.CommentListCreateView.as_view()),
    path('<uuid:uuid>/', views.CommentUpdateDestroyView.as_view()),
]
