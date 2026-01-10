from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UserCharacterForm
from .models import Specialization, UserCharacter


@login_required
def character_list(request):
    """Список персонажей пользователя."""
    characters = UserCharacter.objects.filter(
        user=request.user
    ).select_related("specialization", "specialization__character_class")

    main_character = characters.filter(is_main=True).first()

    # Определяем, из какого контекста идет запрос
    # Если это AJAX или include, показываем только контент
    template_name = "characters/list_full.html"  # По умолчанию полная страница

    # Можно добавить логику для определения контекста
    # Например, по параметру в запросе:
    if request.GET.get("partial") == "true":
        template_name = "characters/list.html"

    context = {
        "characters": characters,
        "characters_count": characters.count(),
        "main_character_name": main_character.name
        if main_character
        else "Нет",
        "title": "Мои персонажи",
    }

    return render(request, template_name, context)


@login_required
def character_create(request):
    """Создание нового персонажа."""
    characters_exists = UserCharacter.objects.filter(
        user=request.user
    ).exists()

    if request.method == "POST":
        form = UserCharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.user = request.user

            # Если это первый персонаж, делаем его основным
            if not characters_exists:
                character.is_main = True

            character.save()

            messages.success(
                request, f"Персонаж {character.name} успешно создан!"
            )
            return redirect("characters:list")
    else:
        form = UserCharacterForm()

        # Если нет персонажей, отмечаем чекбокс по умолчанию
        if not characters_exists:
            form.fields["is_main"].initial = True

    # Получаем все специализации
    specializations = Specialization.objects.select_related(
        "character_class"
    ).order_by("character_class__name", "name")

    context = {
        "form": form,
        "specializations": specializations,
        "characters_exists": characters_exists,
        "title": "Создание персонажа",
    }

    return render(request, "characters/create.html", context)


@login_required
def character_edit(request, pk):
    """Редактирование персонажа."""
    character = get_object_or_404(UserCharacter, pk=pk, user=request.user)

    if request.method == "POST":
        form = UserCharacterForm(request.POST, instance=character)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Персонаж {character.name} успешно обновлен!"
            )
            return redirect("characters:list")
    else:
        form = UserCharacterForm(instance=character)

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
        character_name = character.name
        character.delete()
        messages.success(request, f"Персонаж {character_name} удален.")

    return redirect("characters:list")


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

    return redirect("characters:list")
