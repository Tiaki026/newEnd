# characters/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from characters.models import CharacterClass, Specialization
from characters.constants import CLASSES_DATA


class Command(BaseCommand):
    help = "Заполняет базу данных классами и специализациями из CLASSES_DATA"

    def handle(self, *args, **options):
        self.stdout.write("Начинаем заполнение базы данных...")

        # Создаем классы
        classes_created = 0
        specs_created = 0

        for class_data in CLASSES_DATA:
            # Создаем класс
            class_obj, created = CharacterClass.objects.get_or_create(
                name=class_data["name"]
            )

            if created:
                classes_created += 1
                self.stdout.write(
                    f"✓ Создан класс: {class_obj.get_name_display()}"
                )

            # Создаем специализации для этого класса
            for spec in class_data["specs"]:
                spec_obj, spec_created = Specialization.objects.get_or_create(
                    character_class=class_obj,
                    name=spec["name"],
                    defaults={"role": spec["role"]},
                )

                if spec_created:
                    specs_created += 1
                    self.stdout.write(
                        f'  - Создана специализация: {spec["name"]} ({spec["role"]})'
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"База данных успешно заполнена! "
                f"Создано классов: {classes_created}, специализаций: {specs_created}"
            )
        )
