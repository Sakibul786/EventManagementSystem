from django.urls import path
from . import views

urlpatterns = [
    path(
        "signup/",
        views.signup,
        name="signup",
    ),

    path(
        "login/",
        views.user_login,
        name="login",
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout",
    ),
    path(
        "activate/<uidb64>/<token>/",
        views.activate,
        name="activate",
    ),

     # User Management
    path(
        "users/",
        views.user_list,
        name="user_list",
    ),

    path(
        "users/<int:user_id>/change-role/",
        views.change_role,
        name="change_role",
    ),
    path(
    "users/<int:user_id>/delete/",
    views.delete_user,
    name="delete_user",
    ),
]