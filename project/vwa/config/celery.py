from kombu.utils.url import quote
from decouple import config

aws_access_key = quote(config("AWS_ACCESS_KEY_ID"))
aws_secret_key = quote(config("AWS_SECRET_ACCESS_KEY"))

CELERY_BROKER_URL = f"sqs://{aws_access_key}:{aws_secret_key}@"

CELERY_BROKER_TRANSPORT_OPTIONS = {
    'region': 'sa-east-1',
    'visibility_timeout': 3600,  # Tempo máximo que seu app precia para processar e excluir uma msg da fila
    'queue_name_prefix': 'vwapp-'
}

CELERY_TIMEZONE = "America/Sao_Paulo"
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

if config('CI', default=False):
    CELERY_TASK_ALWAYS_EAGER = True