"""
WSGI config for R4C project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import subprocess


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'R4C.settings')

application = get_wsgi_application()


# Проверка состояния redis и celery
def check_and_start_redis():
    """
    Функция для проверки статуса redis.
    Если redis не запущен, то происходит автоматический запуск
    """
    result = subprocess.run(
        ['systemctl', 'is-active', '--quiet', 'redis'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        subprocess.run(['sudo', 'systemctl', 'start', 'redis'])

def check_and_start_celery():
    """
    Функция для проверки статуса celery.
    Если celery не запущен, то происходит автоматический запуск
    """
    result = subprocess.run(
        ['systemctl', 'is-active', '--quiet', 'celery'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        subprocess.run(['sudo', 'systemctl', 'start', 'celery'])


check_and_start_redis()
check_and_start_celery()
