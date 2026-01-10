from django.urls import path

from . import views

app_name = "characters"

urlpatterns = [
    path("", views.character_list, name="list"),  # Убрал слэш в начале
    path("create/", views.character_create, name="create"),
    path("<int:pk>/edit/", views.character_edit, name="edit"),
    path("<int:pk>/delete/", views.character_delete, name="delete"),
    path("<int:pk>/set-main/", views.set_main_character, name="set_main"),
]
