import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient

DATA_ROOT = os.path.join(settings.BASE_DIR.parent.parent, 'data')
print(DATA_ROOT)


class Command(BaseCommand):
    """
    Скрипт для формирования команды добавки ингредиентов в базу из csv file
    """
    help = 'загружает ингредиенты из csv в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            default='ingredients.csv',
            nargs='?',
            type=str
        )

    def handle(self, *args, **options):
        try:
            with open(os.path.join(DATA_ROOT, options['filename']), 'r',
                      encoding='utf-8') as f:
                data = csv.reader(f)
                for row in data:
                    name, measurement_unit = row
                    Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=measurement_unit
                    )
                print('Загрузка ингредиентов успешно завершена')
        except FileNotFoundError:
            raise CommandError(
                'Добавьте файл ingredients в директорию data\n'
                f'Путь директории {DATA_ROOT}'
            )
