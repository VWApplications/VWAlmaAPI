"""
File to enter application dependencies in development and
production environments
"""

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

APPS = [
    'accounts',
    'core',
    'disciplines'
]

EXTERNAL_APPS = [
    'rest_framework',
    'corsheaders',
    'django_filters',
]

INSTALLED_APPS = DJANGO_APPS + APPS + EXTERNAL_APPS