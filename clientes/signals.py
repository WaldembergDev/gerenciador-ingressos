from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Cliente
from core.tasks import enviar_email_de_confirmacao


@receiver(post_save, sender=Cliente)
def meu_receptor(sender, instance, created, **kwargs):
    if created:
        template = "clientes/emails/email_registro.html"
        destinatario = instance.usuario.email
        contexto = {"nome_usuario": instance.usuario.first_name}
        assunto = "Confirmação de Cadastro"
        enviar_email_de_confirmacao.delay(template, destinatario, assunto, contexto)
