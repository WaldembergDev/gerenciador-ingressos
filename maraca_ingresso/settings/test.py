from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Testes muito mais rápidos na memória
    }
}

USER_AGENT_STRING = f"{APP_NAME}/{APP_VERSION} (ambiente: prod)"

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'