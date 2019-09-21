"""
Django settings for vwa project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

from .config import * # noqa: [F403, F401]
import logging

# Debug
DEBUG = True

try:
    logging.basicConfig(
        filename='vwa/alma.log',
        filemode='w',
        format='[%(asctime)s] [%(levelname)s] [%(pathname)s - %(funcName)s - %(lineno)d]: %(message)s',
        level=logging.INFO
    )
except Exception as error:
    print(error)

# Allow all host/domain to access this aplication
ALLOWED_HOSTS = ['*']

# Urls
ROOT_URLCONF = 'vwa.urls'

# WSGI - Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'vwa.wsgi.application'
