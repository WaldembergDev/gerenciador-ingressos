from celery import shared_task

from integracoes.services import EmailService

@shared_task(bind=True)
def enviar_email_confirmacao_cadastro(self, template, destinatario, assunto, contexto):
    email = EmailService()
    email.enviar_email_de_confirmacao(template, destinatario, assunto, contexto)