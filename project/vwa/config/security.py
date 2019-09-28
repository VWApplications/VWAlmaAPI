# Configurações de desenvolvimento de início rápido - inadequadas para produção
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/
# Torne isso único e não o compartilhe com ninguém.
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'ochn30d!5b#*^-ed%cz8-zuap$wq@joqgu$deg15uusd(kog^^')
