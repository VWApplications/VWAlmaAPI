import datetime

# Django Rest Framework
# http://www.django-rest-framework.org/
REST_FRAMEWORK = {
    # Use a extensão ModHeaders do Chrome para fazer login
    # Authorization: JWT <token>
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

CORS_ORIGIN_ALLOW_ALL = True

SIMPLE_JWT = {
    # Tempo de expiração do token: 1 dia
    # Quando expirado, precisamos obter outro token
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'AUTH_HEADER_TYPES': ('JWT',)
}