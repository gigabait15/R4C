from django.core.management import BaseCommand
from robots.models import Robot
from django.db import connection


test_data = [
    {"model": "D2", "version": "A1"}, {"model": "D2", "version": "D2"}, {"model": "D2", "version": "B3"},
    {"model": "D3", "version": "A1"}, {"model": "D3", "version": "D2"}, {"model": "D3", "version": "B3"},
    {"model": "D2", "version": "A1"}, {"model": "D2", "version": "D2"}, {"model": "D2", "version": "B3"},
    {"model": "D3", "version": "A1"}, {"model": "D3", "version": "D2"}, {"model": "D3", "version": "B3"},
]

class Command(BaseCommand):
    """
    Команда для быстрого заполнение БД данными.
    Данная команда заполняет таблицу robot
    """
    def handle(self, *args, **options):
        # Создание индекса по полю 'model' для быстрого прохода по таблице и получению данных
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_model ON robots_robot(model);
            ''')
            self.stdout.write(self.style.SUCCESS('Индекс по полю "model" был успешно создан.'))

        # Добавление данных из фикстуры
        for entry in test_data:
            Robot.objects.create(
                model=entry['model'],
                version=entry['version'],
            )

        self.stdout.write(self.style.SUCCESS('Фикстуры успешно добавлены в таблицу robots_robot.'))
