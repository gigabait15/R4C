from django.db import models
from R4C.settings import NULLABLE


class Robot(models.Model):
    """
    Модель для создание БД
    Имеет следующие поля:
        serial - текстовый формат поля. флаг unique указывает на уникальность,
            что предотвращает создание модели с таким же номером
        model - текстовый формат поля, обязательный к заполнению.
        version - текстовый формат поля, обязательный к заполнению.
        created - поле формата дата и время. флаг auto_now_add добавляет дату создания автоматически
    """
    serial = models.CharField(max_length=5, unique=True)
    model = models.CharField(max_length=2, **NULLABLE)
    version = models.CharField(max_length=2, **NULLABLE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Robot'
        verbose_name_plural = "Robots"

    def save(self, *args, **kwargs):
        """
        Метод создания и сохранения поля serial
        """
        self.serial = f"{self.model}-{self.version}"
        super().save(*args, **kwargs)

