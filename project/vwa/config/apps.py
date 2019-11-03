DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

ALMA_APPS = [
    'alma.core',
    'alma.disciplines',
    'alma.groups',
    'alma.sections',
    'alma.questions'
]

APPS = ['accounts', 'common']

EXTERNAL_APPS = [
    'rest_framework',
    'corsheaders',
    "anymail"
]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + APPS + ALMA_APPS