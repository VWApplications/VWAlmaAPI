from __future__ import absolute_import, unicode_literals
# from celery.schedules import crontab
from celery import Celery
import os

# Defina o módulo de configurações padrão do Django para o programa 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vwa.settings')

app = Celery('vwa')

# Usar uma string aqui significa que o worker não precisa serializar
# o objeto de configuração para processos filho.
# namespace = 'CELERY' significa que todas as chaves de configuração
# relacionadas ao celery devem ter um prefixo `CELERY_`.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carregue módulos de tarefas (tasks.py) de todas as configurações de aplicativos Django registradas.
app.autodiscover_tasks()

# Tarefas agendadas
# app.conf.beat_schedule = {
#     "ADICIONAR": {
#         "task": "common.tasks.add",
#         'schedule': crontab(),
#         'args': (10, 30)
#     }
# }