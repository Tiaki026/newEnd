from django.core.management.base import BaseCommand
from characters.models import CharacterClass, Specialization
from characters.constants import CLASSES_CHOICES, CLASSES_DATA


class Command(BaseCommand):
    help = "Заполняет базу данных WoW классами, расами и специализациями"

    def handle(self, *args, **options):
        # Создаем классы
        class_objects = {}
        for class_key, class_name in CLASSES_CHOICES:
            obj, created = CharacterClass.objects.get_or_create(name=class_key)
            class_objects[class_key] = obj

        for class_data in CLASSES_DATA:
            character_class = class_objects.get(class_data["name"])
            if character_class:
                for spec in class_data["specs"]:
                    Specialization.objects.get_or_create(
                        character_class=character_class,
                        name=spec["name"],
                        defaults={"role": spec["role"]},
                    )

        self.stdout.write(self.style.SUCCESS("Данные WoW успешно загружены!"))


# python manage.py fill_wow_data
