from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UserCharacterForm
from .models import UserCharacter


@login_required
def character_list(request):
    """Список персонажей пользователя."""
    characters = (
        UserCharacter.objects.filter(user=request.user)
        .select_related("specialization", "specialization__character_class")
        .order_by("-is_main", "-created_at")
    )

    context = {
        "characters": characters,
        "characters_count": characters.count(),
        "title": "Мои персонажи",
    }

    return render(request, "characters/list.html", context)


@login_required
def character_create(request):
    """Создание нового персонажа."""
    if request.method == "POST":
        form = UserCharacterForm(request.POST, user=request.user)
        if form.is_valid():
            character = form.save()
            messages.success(
                request, f"Персонаж {character.name} успешно создан!"
            )
            return redirect("users:profile")
    else:
        form = UserCharacterForm(user=request.user)

    context = {
        "form": form,
        "title": "Создание нового персонажа",
    }
    return render(request, "characters/create.html", context)


@login_required
def character_edit(request, pk):
    """Редактирование персонажа."""
    character = get_object_or_404(UserCharacter, pk=pk, user=request.user)

    if request.method == "POST":
        form = UserCharacterForm(
            request.POST, instance=character, user=request.user
        )
        if form.is_valid():
            character = form.save()
            messages.success(
                request, f"Персонаж {character.name} успешно обновлен!"
            )
            return redirect("users:profile")
    else:
        form = UserCharacterForm(instance=character, user=request.user)

    context = {
        "form": form,
        "character": character,
        "title": f"Редактирование {character.name}",
    }

    return render(request, "characters/edit.html", context)


@login_required
def character_delete(request, pk):
    """Удаление персонажа."""
    character = get_object_or_404(UserCharacter, pk=pk, user=request.user)

    if request.method == "POST":
        # Проверяем, пытаются ли удалить основного персонажа
        if character.is_main:
            # Проверяем, есть ли другие персонажи
            other_characters = UserCharacter.objects.filter(
                user=request.user
            ).exclude(pk=pk)

            if other_characters.exists():
                # Есть другие персонажи - нельзя удалить основного
                messages.error(
                    request,
                    f"Невозможно удалить основного персонажа {character.name}. "
                    f"Сначала назначьте другого персонажа основным.",
                )
            else:
                # Это единственный персонаж - можно удалить
                character_name = character.name
                character.delete()
                messages.success(request, f"Персонаж {character_name} удален.")
        else:
            # Удаляем обычного персонажа
            character_name = character.name
            character.delete()
            messages.success(request, f"Персонаж {character_name} удален.")

    return redirect("users:profile")


@login_required
def set_main_character(request, pk):
    """Установка основного персонажа."""
    character = get_object_or_404(UserCharacter, pk=pk, user=request.user)

    if request.method == "POST":
        # Снимаем основной статус со всех персонажей пользователя
        UserCharacter.objects.filter(user=request.user, is_main=True).update(
            is_main=False
        )

        # Устанавливаем выбранного как основного
        character.is_main = True
        character.save()

        messages.success(
            request, f"{character.name} теперь ваш основной персонаж!"
        )

    return redirect("users:profile")
