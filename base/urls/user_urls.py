from django.urls import path
from base.views import user_views as views

from rest_framework_simplejwt.views import (
    # TODO: Learn to use refresh token and implement it
    TokenObtainPairView,
)

urlpatterns = [
    path("", views.get_users, name="users"),
    path("login/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("profile/", views.get_user_profile, name="users-profile"),
    path("register/", views.register_user, name="register"),
]
