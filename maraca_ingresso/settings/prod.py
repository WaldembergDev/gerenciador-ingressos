from .base import *

DEBUG = False

ALLOWED_HOSTS = ['ingressosmc.pythonanywhere.com']

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

USER_AGENT_STRING = f'{APP_NAME}/{APP_VERSION} (ambiente: prod)'