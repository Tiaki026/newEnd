from django.contrib import admin
from django import forms
from .models import Specialization, UserCharacter


class UserCharacterAdminForm(forms.ModelForm):
    class Meta:
        model = UserCharacter
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["specialization"].queryset = (
                Specialization.objects.all()
            )
        elif not self.instance.pk:
            self.fields["specialization"].queryset = (
                Specialization.objects.all()
            )


@admin.register(UserCharacter)
class UserCharacterAdmin(admin.ModelAdmin):
    form = UserCharacterAdminForm
    list_display = (
        "name",
        "user",
        "get_class",
        "get_spec",
        "get_role",
        "item_level",
        "is_main",
        "created_at",
    )
    list_filter = (
        "specialization__character_class",
        "specialization__role",
        "is_main",
    )
    search_fields = ("name", "user__username", "specialization__name")
    list_editable = ("is_main", "item_level")
    readonly_fields = ("created_at", "get_class_display")

    fieldsets = (
        ("Основное", {"fields": ("name", "user", "is_main")}),
        (
            "Специализация",
            {
                "fields": ("specialization",),
                "description": "При выборе специализации класс определится автоматически",
            },
        ),
        ("Характеристики", {"fields": ("item_level",)}),
        ("Дата", {"fields": ("created_at",)}),
    )

    def get_class(self, obj):
        return obj.specialization.character_class.get_name_display()

    get_class.short_description = "Класс"

    def get_spec(self, obj):
        return obj.specialization.name

    get_spec.short_description = "Специализация"

    def get_role(self, obj):
        return obj.specialization.get_role_display()

    get_role.short_description = "Роль"

    def get_class_display(self, obj):
        if obj.specialization:
            return obj.specialization.character_class.get_name_display()
        return "Не выбрано"

    def save_model(self, request, obj, form, change):
        """Сохраняем с проверкой."""
        obj.clean()
        super().save_model(request, obj, form, change)
