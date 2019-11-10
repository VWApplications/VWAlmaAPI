from decouple import config

rabbitmq_user = config('RABBITMQ_USER', default='vwapp')
rabbitmq_password = config('RABBITMQ_PASSWORD', default='vwapp')
rabbitmq_host = config('NEW_RABBITMQ_HOST', default='rabbitmq:5672')
rabbitmq_vhost = config('RABBITMQ_VHOST', default='vwapp_vhost')

CELERY_BROKER_URL = f'amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}/{rabbitmq_vhost}'

CELERY_TIMEZONE = "America/Sao_Paulo"

if config('CI', default=False):
    CELERY_TASK_ALWAYS_EAGER = True