"""
Configuração WSGI para o projeto alma.

Ele expõe o WSGI que pode ser chamado como uma variável no nível do módulo chamada `` application``.

Para mais informações, veja:
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vwa.settings')

application = get_wsgi_application()
