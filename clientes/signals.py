from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Cliente
from .tasks import enviar_email_confirmacao_cadastro


@receiver(post_save, sender=Cliente)
def confirmacao_cadastro(sender, instance, created, **kwargs):
    if created:
        template = "clientes/emails/email_registro.html"
        destinatario = instance.usuario.email
        contexto = {"nome_usuario": instance.usuario.first_name}
        assunto = "Confirmação de Cadastro"
        enviar_email_confirmacao_cadastro.delay(template, destinatario, assunto, contexto)
