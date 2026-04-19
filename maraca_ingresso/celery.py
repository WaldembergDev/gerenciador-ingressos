import os
from celery import Celery
from decouple import config

settings_path = config("PATH_SETTINGS", default="maraca_ingresso.settings.dev")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_path)

app = Celery("maraca_ingresso")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
