from django.urls import path
from . import views


urlpatterns = [
    path('', views.ReviewListCreateView.as_view()),
    path('<uuid:uuid>/', views.ReviewUpdateDestroyView.as_view()),
]
