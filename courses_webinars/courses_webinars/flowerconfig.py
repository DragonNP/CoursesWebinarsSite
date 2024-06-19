from decouple import config

RABBITMQ_HOST = config('RABBITMQ_HOST')
RABBITMQ_USER = config('RABBITMQ_CELERY_USER')
RABBITMQ_PASSWORD = config('RABBITMQ_CELERY_PASSWORD')

broker_api = f'http://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:15672/api/'
persistent = True
