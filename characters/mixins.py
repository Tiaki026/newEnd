from django.core.exceptions import ValidationError


class CharacterClassMixin:
    """Миксин для получения класса персонажа."""

    @property
    def character_class(self):
        return self.specialization.character_class


class MainCharacterMixin:
    """Миксин для работы с основным персонажем."""

    def clean(self):
        super().clean()
        self._validate_main_character()

    def _validate_main_character(self):
        """Валидация основного персонажа."""
        if self.is_main and not self.user:
            raise ValidationError(
                "Основным персонажем может быть только персонаж с владельцем."
            )

    def save(self, *args, **kwargs):
        """Логика сохранения основного персонажа."""
        from .models import UserCharacter

        if self.is_main and self.user:
            UserCharacter.objects.filter(user=self.user, is_main=True).update(
                is_main=False
            )

        super().save(*args, **kwargs)
