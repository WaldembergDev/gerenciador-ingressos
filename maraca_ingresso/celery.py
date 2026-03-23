import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maraca_ingresso.settings")

app = Celery("maraca_ingresso")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
