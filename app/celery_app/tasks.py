from time import sleep

from celery import Celery

app = Celery('tasks')
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/1'


@app.task
def add(x: int, y: int) -> int:
    sleep(2)
    return x + y

# celery -A tasks.py  worker --loglevel=INFO
