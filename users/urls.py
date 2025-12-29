# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"  # Пространство имен для этого приложения

urlpatterns = [

    # Регистрация
    path("register/", views.register, name="register"),
    # Вход/выход (можно использовать стандартные представления Django)
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="users/login.html",
            redirect_authenticated_user=True,  # Если уже авторизован, перенаправляем
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    # Профиль пользователя
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    # Смена пароля
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password_change.html", success_url="done/"
        ),
        name="password_change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html"
        ),
        name="password_change_done",
    ),
]
