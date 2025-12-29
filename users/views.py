# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User




def register(request):
    """Регистрация нового пользователя"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически входим после регистрации
            messages.success(
                request, "Регистрация прошла успешно! Добро пожаловать!"
            )
            return redirect("characters:list")  # Перенаправляем к персонажам
    else:
        form = UserCreationForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    """Профиль пользователя"""
    user = request.user
    # Можно добавить статистику пользователя
    return render(request, "users/profile.html", {"user": user})


@login_required
def profile_edit(request):
    """Редактирование профиля"""
    if request.method == "POST":
        # Здесь можно добавить форму для редактирования профиля
        pass
    return render(request, "users/profile_edit.html")
