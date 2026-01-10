from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from .constants import CLASSES_CHOICES, ROLE_CHOICES
from .mixins import CharacterClassMixin, MainCharacterMixin

User = get_user_model()


class CharacterClass(models.Model):
    """Класс персонажа."""

    name = models.CharField(
        max_length=50,
        choices=CLASSES_CHOICES,
        unique=True,
        verbose_name="Класс",
    )

    class Meta:
        verbose_name = "Класс"
        verbose_name_plural = "Классы"

    def __str__(self) -> str:
        return self.get_name_display()


class Specialization(models.Model):
    """Специализация персонажа."""

    character_class = models.ForeignKey(
        CharacterClass,
        on_delete=models.CASCADE,
        related_name="specializations",
        verbose_name="Класс",
    )
    name = models.CharField(max_length=50, verbose_name="Специализация")
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        verbose_name="Роль",
    )

    class Meta:
        verbose_name = "Специализация"
        verbose_name_plural = "Специализации"
        unique_together = [("character_class", "name")]

    def __str__(self) -> str:
        return f"{self.name} ({self.character_class.get_name_display()})"


class UserCharacter(CharacterClassMixin, MainCharacterMixin, models.Model):
    """Персонаж пользователя."""

    name = models.CharField(
        max_length=16,
        verbose_name="Имя персонажа",
        help_text="2-16 символов",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="characters",
        verbose_name="Владелец",
        null=True,
        blank=True,
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.PROTECT,
        related_name="characters",
        verbose_name="Специализация",
    )
    item_level = models.IntegerField(
        default=600,
        validators=[MinValueValidator(600)],
        verbose_name="Уровень предметов",
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name="Основной персонаж",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"
        ordering = ["-created_at"]
        unique_together = [("name", "user")]
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(is_main=True),
                name="unique_main_character_per_user",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({
            self.specialization.character_class.get_name_display()
        })"


very_long_variable_name = (
    "Это очень длинная строка, которая точно превышает 79 символов и должна "
    "быть разбита на несколько строк автоматически при "
    "форматировании"
)
