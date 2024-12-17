from unittest.mock import patch
from django.test import TestCase, Client
from django.urls.base import reverse
from robots.models import Robot


class RobotsTest(TestCase):
    """
    Класс для тестированые request запросов для view класса Robot
    """
    def setUp(self):
        """
        Данные для тестов
        """
        self.url_list = reverse('robots:view_robots')
        self.url_create = reverse('robots:create_robot')
        self.client = Client()
        self.url = reverse('robots:download_weekly_report')

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

    @patch('django.core.management.call_command')
    @patch('os.path.exists')
    def test_download_weekly_report_success(self, mock_exists, mock_call_command):
        """
        Тестируем успешное создание и загрузку отчета.
        """

        # Имитация успешного вызова команды и существования файла
        mock_call_command.return_value = 'weekly_report_2024-12-10_to_2024-12-17.xlsx'
        mock_exists.return_value = True

        # Выполнение запроса
        response = self.client.get(self.url)

        # Проверка статуса
        self.assertEqual(response.status_code, 200)

        # Проверка типа контента
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # Проверка заголовков
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=weekly_report_2024-12-10_to_2024-12-17.xlsx')

        # Проверка содержимого ответа (сообщение)
        expected_message = "Отчет 'weekly_report_2024-12-10_to_2024-12-17.xlsx' успешно создан и готов для скачивания."
        self.assertIn(expected_message.encode('utf-8'),
                      response.content)  # Преобразуем строку в bytes с кодировкой utf-8

    @patch('django.core.management.call_command')
    @patch('os.path.exists')
    def test_download_weekly_report_file_not_found(self, mock_exists, mock_call_command):
        """
        Тестируем ситуацию, когда файл отчета не найден.
        """

        # Имитация вызова команды, но файл не существует
        mock_call_command.return_value = 'weekly_report.xlsx'
        mock_exists.return_value = False

        # Выполнение запроса
        response = self.client.get(self.url)

        # Проверка статуса
        self.assertEqual(response.status_code, 404)

        # Проверка содержимого ответа (сообщение о файле не найдено)
        self.assertEqual(response.content.decode(), "Отчет не найден")
