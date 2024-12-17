from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from orders.models import Order
from robots.models import Robot


@shared_task
def check_robot():
    """
    Функция для просмотра доступности робота для заказов в ожидании
    Получает все заказы с ожиданием(status = True), проверяет по номеру наличие робота
    """
    orders_status = Order.objects.filter(status=True)

    for order in orders_status:
        try:
            robot = Robot.objects.get(serial=order.robot_serial)
            if robot.sold is False:
                send_mail(order.customer.email, robot)

        except Robot.DoesNotExist:
            continue

def send_email(customer_email, robot):
    subject = 'Добрый день!'
    message = (f'Недавно вы интересовались нашим роботом модели {robot.model}, версии {robot.version}. \n'
               f'Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами')
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [customer_email])