from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HistoricoCompra
from .tasks import enviar_notificacao_whatsapp, enviar_email_confirmacao_pagamento
from .utils import criar_mensagem_whatsapp
from django.conf import settings


@receiver(post_save, sender=HistoricoCompra)
def pagamento_aprovado(sender, instance, created, **kwargs):
    if instance.status == HistoricoCompra.Status.APROVADO.value:
        # enviando notificação de Whatsapp para o administrador
        mensagem = criar_mensagem_whatsapp(
            instance.id,
            instance.titulo,
            instance.data_horario_evento.strftime("%d/%m/%Y %H:%M"),
            instance.quantidade,
            instance.valor_pago,
            instance.cliente.usuario.first_name,
        )
        numero = settings.NUMERO_NOTIFICACAO
        enviar_notificacao_whatsapp.delay(numero, mensagem)
        # enviando notificação para o cliente
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
        enviar_email_confirmacao_pagamento.delay(
            template, destinatario, assunto, contexto
        )
