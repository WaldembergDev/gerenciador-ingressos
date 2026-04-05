from django.apps import AppConfig


class IngressosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ingressos"

    def ready(self):
        import ingressos.signals
