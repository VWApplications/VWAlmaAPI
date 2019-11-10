from __future__ import absolute_import, unicode_literals
# Isso garantirá que o aplicativo seja sempre importado quando o
# Django for iniciado, para que o shared_task o utilize
from .celery import app as celery_app

__all__ = ('celery_app',)