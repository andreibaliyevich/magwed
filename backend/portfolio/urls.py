from django.urls import path, include
from . import views


urlpatterns = [
    path('album/', include([
        path('author/', include([
            path('list-create/', views.AlbumListCreateView.as_view()),
            path('image-update/<uuid:uuid>/',
                views.AlbumImageUpdateView.as_view()),
            path('rud/<uuid:uuid>/', views.AlbumRUDView.as_view()),
        ])),
        path('list/', views.AlbumListView.as_view()),
        path('retrieve/<uuid:uuid>/', views.AlbumRetrieveView.as_view()),
        path('up-view-count/<uuid:uuid>/',
            views.AlbumUpViewCountView.as_view()),
        path('like/<uuid:uuid>/', views.AlbumLikeView.as_view()),
    ])),

    path('photo/', include([
        path('author/', include([
            path('list-create/', views.PhotoListCreateView.as_view()),
            path('rud/<uuid:uuid>/', views.PhotoRUDView.as_view()),
        ])),
        path('list/', views.PhotoListView.as_view()),
        path('retrieve/<uuid:uuid>/', views.PhotoRetrieveView.as_view()),
        path('up-view-count/<uuid:uuid>/',
            views.PhotoUpViewCountView.as_view()),
        path('like/<uuid:uuid>/', views.PhotoLikeView.as_view()),
    ])),
]
