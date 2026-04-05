from celery import shared_task
import logging
from integracoes.services import Whapi, EmailService

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def enviar_notificacao_whatsapp(self, numero: str, message: str):
    whapi = Whapi()
    whapi.send_message_text(numero, message)
    logger.info('Task de notificacao finalizada')


@shared_task(bind=True)
def enviar_email_confirmacao_pagamento(self, template, destinatario, assunto, contexto):
    email = EmailService()
    email.enviar_email_de_confirmacao(template, destinatario, assunto, contexto)
    logger.info('Task de confirmação de pagamento finalizada')
