from django.urls import path, include
from . import views


urlpatterns = [
    path('auth/', include([
        path('login/', views.LoginView.as_view()),
        path('logout/', views.LogoutView.as_view()),
        path('registration/', views.RegistrationView.as_view()),
        path('activation/', views.ActivationView.as_view()),
        path('password/', include([
            path('change/', views.PasswordChangeView.as_view()),
            path('reset/', include([
                path('', views.PasswordResetView.as_view()),
                path('confirm/', views.PasswordResetConfirmView.as_view()),
            ])),
        ])),
        path('profile/', views.ProfileView.as_view()),
        path('avatar/', views.ProfileAvatarView.as_view()),
        path('cover/', views.OrganizerCoverView.as_view()),
    ])),
    path('organizers/', include([
        path('', views.OrganizerListView.as_view()),
        path('cost-work-min-max/', views.CostWorkMinMaxView.as_view()),
        path('<slug:profile_url>/', views.OrganizerRetrieveView.as_view()),
    ])),
]
