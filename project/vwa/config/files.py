import os

# Crie caminhos dentro do projeto como este: /vwa/config/files.py
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

STATIC_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# O caminho absoluto para os arquivos estáticos coletados
# Ex: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(STATIC_DIR, 'common/staticfiles')

# Prefixo da URL para arquivos estáticos
# Ex: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# O caminho absoluto para os arquivos dinâmicos coletados
# Ex: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# Prefixo da URL para arquivos dinâmicos
# Ex: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'