import datetime

# Django Rest Framework
# http://www.django-rest-framework.org/
REST_FRAMEWORK = {
    # Use the extension ModHeaders of Chrome to login
    # Authorization: JWT <token>
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

CORS_ORIGIN_ALLOW_ALL = True

SIMPLE_JWT = {
    # Expiration time of token: 30 min
    # When expirated we need to get another token
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'AUTH_HEADER_TYPES': ('JWT',)
}