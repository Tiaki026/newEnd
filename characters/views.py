# characters/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import UserCharacter, CharacterClass, Specialization
from .forms import UserCharacterForm


class CharacterListView(LoginRequiredMixin, ListView):
    """Список персонажей пользователя"""

    model = UserCharacter
    template_name = "characters/list.html"
    context_object_name = "characters"

    def get_queryset(self):
        return (
            UserCharacter.objects.filter(user=self.request.user)
            .select_related(
                "specialization", "specialization__character_class"
            )
            .order_by("-is_main", "-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_character"] = (
            self.get_queryset().filter(is_main=True).first()
        )
        return context


@login_required
def character_create(request):
    """Создание нового персонажа"""
    if request.method == "POST":
        form = UserCharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.user = request.user

            # Если делаем основным, снимаем флаг с других
            if character.is_main:
                UserCharacter.objects.filter(
                    user=request.user, is_main=True
                ).update(is_main=False)

            character.save()
            messages.success(
                request, f'Персонаж "{character.name}" успешно создан!'
            )
            return redirect("characters:detail", pk=character.pk)
    else:
        form = UserCharacterForm()

    # Для динамического выбора специализаций
    specializations = Specialization.objects.select_related(
        "character_class"
    ).all()

    return render(
        request,
        "characters/create.html",
        {
            "form": form,
            "specializations": specializations,
        },
    )


class CharacterDetailView(LoginRequiredMixin, DetailView):
    """Детальная информация о персонаже"""

    model = UserCharacter
    template_name = "characters/detail.html"
    context_object_name = "character"

    def get_queryset(self):
        # Пользователь может видеть только своих персонажей
        return UserCharacter.objects.filter(user=self.request.user)


@login_required
def character_edit(request, pk):
    """Редактирование персонажа"""
    character = get_object_or_404(UserCharacter, pk=pk, user=request.user)

    if request.method == "POST":
        form = UserCharacterForm(request.POST, instance=character)
        if form.is_valid():
            updated_character = form.save()
            messages.success(
                request, f'Персонаж "{updated_character.name}" обновлен!'
            )
            return redirect("characters:detail", pk=character.pk)
    else:
        form = UserCharacterForm(instance=character)

    return render(
        request,
        "characters/edit.html",
        {
            "form": form,
            "character": character,
        },
    )


@login_required
def character_delete(request, pk):
    """Удаление персонажа"""
    character = get_object_or_404(UserCharacter, pk=pk, user=request.user)

    if request.method == "POST":
        character_name = character.name
        character.delete()
        messages.success(request, f'Персонаж "{character_name}" удален!')
        return redirect("characters:list")

    return render(
        request,
        "characters/delete_confirm.html",
        {
            "character": character,
        },
    )


@login_required
@require_http_methods(["POST"])
def set_main_character(request, pk):
    """Установка основного персонажа (AJAX или обычный запрос)"""
    character = get_object_or_404(UserCharacter, pk=pk, user=request.user)

    # Снимаем флаг с других персонажей
    UserCharacter.objects.filter(user=request.user, is_main=True).update(
        is_main=False
    )

    # Устанавливаем флаг текущему
    character.is_main = True
    character.save()

    messages.success(
        request, f'"{character.name}" теперь ваш основной персонаж!'
    )

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True})

    return redirect("characters:list")


def get_specializations(request, class_id):
    """API для получения специализаций по классу (для AJAX)"""
    specializations = Specialization.objects.filter(
        character_class_id=class_id
    ).values("id", "name", "role")

    return JsonResponse(list(specializations), safe=False)
