# flake8: noqa
from .apps import INSTALLED_APPS
from .database import DATABASES
from .files import STATIC_ROOT, STATIC_URL, MEDIA_ROOT, MEDIA_URL
from .internacionalization import LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_L10N, USE_TZ
from .middleware import MIDDLEWARE
from .password import AUTH_PASSWORD_VALIDATORS
from .rest import REST_FRAMEWORK, CORS_ORIGIN_ALLOW_ALL, SIMPLE_JWT
from .security import SECRET_KEY
from .template import TEMPLATES
from .users import AUTH_USER_MODEL
from .email import EMAIL_BACKEND, ANYMAIL, DEFAULT_FROM_EMAIL
from .sentry import *
from .storage import *