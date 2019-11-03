from decouple import config

POSTGRES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('POSTGRES_DB', default="vwapp_db"),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST', default="postgres"),
        'PORT': config('POSTGRES_PORT', default="5432")
    }
}

DATABASES = POSTGRES