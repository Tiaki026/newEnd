from django import forms

from .models import Specialization, UserCharacter


# Упрощенная версия - одна форма для всего
class UserCharacterForm(forms.ModelForm):
    is_main = forms.BooleanField(
        required=False,
        label="Сделать основным персонажем",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = UserCharacter
        fields = ["name", "specialization", "is_main"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите имя персонажа",
                    "maxlength": "16",
                    "minlength": "2",
                }
            ),
            "specialization": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }
        labels = {
            "name": "Имя персонажа",
            "specialization": "Специализация",
            "is_main": "Сделать основным персонажем",
        }
        help_texts = {
            "name": "2-16 символов",
            "is_main": "Если отметить, этот персонаж станет вашим основным",
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Настраиваем поле специализации
        self.fields[
            "specialization"
        ].queryset = Specialization.objects.select_related(
            "character_class"
        ).all()
        self.fields["specialization"].empty_label = "Выберите специализацию"

        # Если персонаж уже основной
        if self.instance and self.instance.pk and self.instance.is_main:
            self.fields["is_main"].initial = True
            self.fields["is_main"].widget = forms.HiddenInput()
            self.fields[
                "is_main"
            ].help_text = "Этот персонаж уже является вашим основным"

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name and self.user:
            # Проверка на уникальность
            query = UserCharacter.objects.filter(
                user=self.user, name__iexact=name
            )
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)

            if query.exists():
                raise forms.ValidationError(
                    "У вас уже есть персонаж с таким именем"
                )
        return name

    def save(self, commit=True):
        character = super().save(commit=False)

        # Устанавливаем пользователя для нового персонажа
        if not character.pk:
            character.user = self.user

        # Обработка основного персонажа
        make_main = self.cleaned_data.get("is_main", False)

        if make_main:
            # Если отмечаем как основного
            UserCharacter.objects.filter(user=self.user, is_main=True).update(
                is_main=False
            )
            character.is_main = True
        elif not character.pk:
            # Если это новый персонаж и он не отмечен как основной,
            # проверяем, есть ли у пользователя другие персонажи
            if not UserCharacter.objects.filter(user=self.user).exists():
                character.is_main = True

        if commit:
            character.save()

        return character
