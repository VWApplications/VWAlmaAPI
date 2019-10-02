# Configurações de desenvolvimento de início rápido - inadequadas para produção
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/
# Torne isso único e não o compartilhe com ninguém.
from decouple import config

SECRET_KEY = config('SECRET_KEY')
