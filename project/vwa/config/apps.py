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
    'corsheaders'
]

INSTALLED_APPS = DJANGO_APPS + APPS + EXTERNAL_APPS