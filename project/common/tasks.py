from __future__ import absolute_import, unicode_literals
from vwa.celery import app


@app.task(bind=True, max_retries=3)
def add(self, x, y):
    """
    Tarefa assíncrona.
    add.delay(10, 20)
    """

    print("ENTREIII")
    return x + y