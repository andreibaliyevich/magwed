from django.urls import path
from . import views


urlpatterns = [
    path('currencies/<str:code>/', views.CurrencyRetrieveView.as_view()),
    path('cities/', views.CityListView.as_view()),
    path('magazine/', views.MagazineView.as_view()),
    path('tags/<uuid:uuid>/', views.TagRetrieveView.as_view()),
]
