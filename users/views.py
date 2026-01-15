from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from characters.models import Specialization, UserCharacter

from .forms import CreationForm, DeleteAccountForm, ProfileUpdateForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("users:login")
    template_name = "users/signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем все специализации из БД
        # Сортируем по классу и названию
        context["specializations"] = Specialization.objects.select_related(
            "character_class"
        ).order_by("character_class__name", "name")
        return context


def only_user_view(request):
    if not request.user.is_authenticated:
        return redirect("/auth/login/")


@login_required
def profile(request):
    """Страница профиля пользователя."""
    # Обработка обновления профиля
    if request.method == "POST" and "update_profile" in request.POST:
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен!")
            return redirect("users:profile")

    # Получаем персонажей пользователя
    characters = UserCharacter.objects.filter(
        user=request.user
    ).select_related("specialization", "specialization__character_class")

    # Получаем специализации для формы создания
    specializations = Specialization.objects.select_related(
        "character_class"
    ).order_by("character_class__name", "name")

    # Основной персонаж
    main_character = characters.filter(is_main=True).first()

    # Форма для обновления профиля
    profile_form = ProfileUpdateForm(instance=request.user)

    context = {
        "characters": characters,
        "characters_count": characters.count(),
        "main_character_name": (
            main_character.name if main_character else "Нет"
        ),
        "specializations": specializations,
        "main_character_class": (
            main_character.specialization.character_class.get_name_display()
            if main_character
            else None
        ),
        "main_specialization_name": main_character.specialization.name
        if main_character
        else None,
        "profile_form": profile_form,
        "title": f"Профиль | {request.user.username}",
    }

    return render(request, "users/profile.html", context)


@login_required
def update_profile(request):
    """Обновление профиля пользователя."""
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен!")
            return redirect("users:profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(
        request,
        "users/profile_update.html",
        {"form": form, "title": "Обновление профиля"},
    )


@login_required
def delete_account(request):
    """Удаление аккаунта пользователя."""
    if request.method == "POST":
        form = DeleteAccountForm(request.user, request.POST)
        if form.is_valid():
            # Сохраняем имя пользователя для сообщения
            username = request.user.username

            # Удаляем аккаунт
            request.user.delete()

            # Разлогиниваем пользователя
            from django.contrib.auth import logout

            logout(request)

            messages.success(request, f"Аккаунт {username} успешно удален.")
            return redirect("posts:index")
    else:
        form = DeleteAccountForm(request.user)

    return render(
        request,
        "users/delete_account.html",
        {"form": form, "title": "Удаление аккаунта"},
    )
