from django.urls import path, include
from . import views


urlpatterns = [
    path('links/', include([
        path('', views.SocialLinkListCreateView.as_view()),
        path('<uuid:uuid>/', views.SocialLinkUpdateDestroyView.as_view()),
    ])),
    path('follow/', include([
        path('user/<uuid:uuid>/', views.FollowCreateDestroyView.as_view()),
        path('list/', views.FollowListView.as_view()),
        path('related-users/', views.RelatedUserListView.as_view()),
    ])),
    path('favorite/', include([
        path('', views.FavoriteCreateDestroyView.as_view()),
        path('list/', views.FavoriteListView.as_view()),
    ])),
]
