DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

ACCOUNTS_APPS = [
    'accounts',
    'alma.accounts.apps.AlmaAccountsConfig'
]

ALMA_APPS = [
    'alma.core',
    'alma.disciplines',
    'alma.groups',
    'alma.sections',
    'alma.questions'
]

GENERIC_APPS = ['common']

EXTERNAL_APPS = [
    'rest_framework',
    'corsheaders',
    "anymail"
]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + ACCOUNTS_APPS + GENERIC_APPS + ALMA_APPS