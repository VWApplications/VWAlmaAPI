from .config import * # noqa: [F403, F401]
from decouple import config
import logging

# Debug
DEBUG = config('DEBUG', default=False, cast=bool)

try:
    logging.basicConfig(
        filename='vwa/alma.log',
        filemode='a',
        format='[%(asctime)s] [%(levelname)s] [%(pathname)s - %(funcName)s - %(lineno)d]: %(message)s',
        level=logging.INFO
    )
except Exception as error:
    print(error)

# Permitir que todo host/domínio acesse este aplicativo
ALLOWED_HOSTS = ['*']

# Urls
ROOT_URLCONF = 'vwa.urls'

# WSGI - Caminho pontilhado do Python para o aplicativo WSGI usado pelo servidor de execução do Django.
WSGI_APPLICATION = 'vwa.wsgi.application'
