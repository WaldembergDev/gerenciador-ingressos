from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HistoricoCompra
from .tasks import enviar_notificacao
from datetime import datetime
from django.conf import settings
from core.tasks import enviar_email_de_confirmacao


@receiver(post_save, sender=HistoricoCompra)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        # enviando notificação de Whatsapp para o administrador
        numero = settings.NUMERO_NOTIFICACAO
        evento = instance.titulo
        data_evento = datetime.strftime(instance.data_horario_evento, "%d/%m/%Y %H:%M")
        enviar_notificacao.delay(numero, evento, data_evento)
        # enviando notificação ao responsável pela compra
        template = "ingressos/emails/email_confirmacao_compra.html"
        destinatario = instance.cliente.usuario.email
        assunto = "Confirmação de Compra"
        contexto = {
            "nome_usuario": instance.cliente.usuario.first_name,
            "titulo": instance.titulo,
            "data_horario_evento": instance.data_horario_evento,
            "valor_pago": instance.valor_pago,
            "quantidade": instance.quantidade,
            "local": instance.local,
        }
        enviar_email_de_confirmacao.delay(template, destinatario, assunto, contexto)
