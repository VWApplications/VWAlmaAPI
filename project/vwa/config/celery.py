from kombu.utils.url import quote
from decouple import config

aws_access_key = quote(config("AWS_ACCESS_KEY_ID"))
aws_secret_key = quote(config("AWS_SECRET_ACCESS_KEY"))

CELERY_BROKER_URL = f"sqs://{aws_access_key}:{aws_secret_key}@"

CELERY_BROKER_TRANSPORT_OPTIONS = {
    'region': 'sa-east-1',
    'visibility_timeout': 3600,
    'polling_interval': 20,
    'queue_name_prefix': 'vwapp-'
}

CELERY_TIMEZONE = "America/Sao_Paulo"
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"

if config('CI', default=False):
    CELERY_TASK_ALWAYS_EAGER = True