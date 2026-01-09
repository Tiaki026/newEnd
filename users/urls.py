from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    path(
        'logout/',
        LogoutView.as_view(
            template_name='index.html',
            next_page='index',
        ),
        name='logout'
    ),
    path(
        'signup/',
        views.SignUp.as_view(extra_context={'title': 'Присоединиться | END'}),
        name='signup'
    ),
    path(
        'login/',
        LoginView.as_view(
            template_name='users/login.html',
            extra_context={'title': 'Вход | END'}
        ),
        name='login'
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(
            template_name='users/password_reset_form.html',
            extra_context={'title': 'Сброс пароля | END'}
        ),
        name='password_reset_form'
    ),
    path(
        'password_change/form/',
        PasswordChangeView.as_view(
            template_name='users/password_change_form.html',
            extra_context={'title': 'Смена пароля | END'}
        ),
        name='password_change_form'
    ),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html',
            extra_context={'title': 'Пароль изменен | END'}
        ),
        name='password_change_done'
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html',
            extra_context={'title': 'Письмо отправлено | END'}
        ),
        name='password_reset_done'
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
            extra_context={'title': 'Пароль сброшен | END'}
        ),
        name='password_reset_complete'
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            extra_context={'title': 'Новый пароль | END'}
        ),
        name='password_reset_confirm'
    ),
]
