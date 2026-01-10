from django import forms

from .models import UserCharacter


class UserCharacterForm(forms.ModelForm):
    class Meta:
        model = UserCharacter
        fields = ["name", "specialization", "is_main"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите имя персонажа (2-16 символов)",
                    "maxlength": "16",
                    "minlength": "2",
                }
            ),
            "specialization": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_specialization",
                }
            ),
            "is_main": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Можно добавить сортировку или фильтрацию специализаций
        self.fields["specialization"].queryset = self.fields[
            "specialization"
        ].queryset.select_related("character_class")
