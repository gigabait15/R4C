from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls.base import reverse
from robots.models import Robot


class RobotsTest(TestCase):
    """
    Класс для тестированые request запросов для view класса Robot
    """
    def setUp(self):
        self.url_list = reverse('robots:view_robots')
        self.url_create = reverse('robots:create_robot')

    def test_robots_view(self):
        """
        Метод для тестирование представления отображения всех экземпляров из БД.
        Проверка на статус код 200, проверка на путь и отсутсвия ошибок при подключении
        """
        url = self.url_list
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], url)
        self.assertNotContains(response, 'Error')

    def test_create_robot(self):
        """
        Тестируем создание нового робота через POST запрос.
        Проверка на ответ после запроса, проверка на появления модели в БД
        """
        data = {
            'model': 'R2',
            'version': 'D2',
        }
        url = self.url_create
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Robot.objects.count(), 1)

        robot = Robot.objects.first()
        self.assertEqual(robot.model, 'R2')
        self.assertEqual(robot.version, 'D2')
        self.assertEqual(robot.serial, 'R2-D2')

    def test_create_duplicate_robot(self):
        """
        Тестируем создание робота с дублирующимися данными.
        Проверка на дубликаты, при создании такого же экземляра ошибка
        """
        data = {
            'model': 'R2',
            'version': 'D2',
        }
        url = self.url_create
        self.client.post(url, data)

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Robot.objects.count(), 1)