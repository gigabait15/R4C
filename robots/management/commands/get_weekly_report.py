from django.core.management import BaseCommand
from robots.models import Robot
from django.db import models
import pandas as pd
from datetime import datetime, timedelta
import os
from django.conf import settings


class Command(BaseCommand):
    """
    Комадна для создания недельного отчета по производству.
    Для создания excel файла с постраничным отображениям используется pandas
    """
    def handle(self, *args, **options):
        # определенние временных диапазонов
        today = datetime.today()
        end_of_week = today
        start_of_week = today - timedelta(days=7)
        start_of_week_str = start_of_week.strftime('%Y-%m-%d')
        end_of_week_str = end_of_week.strftime('%Y-%m-%d')

        try:
            # Получение данные из базы данных за последние 7 дней
            robots = Robot.objects.filter(
                created__gte=start_of_week,
                created__lte=end_of_week
            ).values('model', 'version').annotate(quantity=models.Count('id'))

            # Преобразование данные в DataFrame
            data = pd.DataFrame(list(robots))

            # Именование колонок согласно ТЗ
            data = data.rename(columns={
                'model': 'Модель',
                'version': 'Версия',
                'quantity': 'Количество за неделю'
            })

            if not data.empty:
                # Путь к файлу
                report_filename = f"weekly_report_{start_of_week_str}_to_{end_of_week_str}.xlsx"
                # Сохранение пути в переменной для дальнейшей обработки в view
                report_filepath = os.path.join(settings.MEDIA_ROOT, report_filename)

                # Создание Excel writer
                with pd.ExcelWriter(report_filepath, engine='openpyxl') as writer:
                    grouped_data = data.groupby('Модель')

                    for model, group in grouped_data:
                        # Запись данных на отдельный лист для каждой модели
                        group.to_excel(writer, sheet_name=model, index=False)

                    self.stdout.write(self.style.SUCCESS(f"Недельный отчет успешно сохранен в {report_filepath}."))

                return report_filepath

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Произошла ошибка при генерации отчета: {str(e)}"))
            return None
