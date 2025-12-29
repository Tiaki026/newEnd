# characters/urls.py
from django.urls import path
from . import views

app_name = "characters"  # Пространство имен для этого приложения

urlpatterns = [
    # Список персонажей пользователя
    path("", views.CharacterListView.as_view(), name="list"),
    # Создание нового персонажа
    path("create/", views.character_create, name="create"),
    # Детали персонажа (по ID)
    path("<int:pk>/", views.CharacterDetailView.as_view(), name="detail"),
    # Редактирование персонажа
    path("<int:pk>/edit/", views.character_edit, name="edit"),
    # Удаление персонажа
    path("<int:pk>/delete/", views.character_delete, name="delete"),
    # Установка основного персонажа (AJAX или обычный запрос)
    path("<int:pk>/set-main/", views.set_main_character, name="set_main"),
    # API для получения специализаций по классу (для AJAX)
    path(
        "api/specs/<int:class_id>/",
        views.get_specializations,
        name="api_specs",
    ),
]
