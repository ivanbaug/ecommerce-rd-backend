from django.urls import path
from base.views import user_views as views

from rest_framework_simplejwt.views import (
    # TODO: Learn to use refresh token and implement it
    TokenObtainPairView,
)

urlpatterns = [
    path("", views.get_users, name="users"),
    path("login/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("profile/", views.get_user_profile, name="user-profile"),
    path("profile/update/", views.update_user_profile, name="user-profile-update"),
    path("register/", views.register_user, name="register"),
    path("update/<str:pk>/", views.update_user, name="user-update"),
    path("<str:pk>/", views.get_user_by_id, name="user"),
    path("delete/<str:pk>/", views.delete_user, name="user-delete"),
]
