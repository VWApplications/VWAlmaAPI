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
    'disciplines',
    'groups',
    'sections'
]

EXTERNAL_APPS = [
    'rest_framework',
    'corsheaders',
    "anymail"
]

INSTALLED_APPS = DJANGO_APPS + APPS + EXTERNAL_APPS