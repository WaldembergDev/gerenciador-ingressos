from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from celery import shared_task


@shared_task(name="enviar_notificacao", bind=True)
def enviar_email_de_confirmacao(self, template, destinatario, assunto, contexto):
    # 1. Definir o contexto para o template
    context = contexto

    # 2. Renderizar o template HTML para uma string
    html_content = render_to_string(template, context)

    # 3. Gerar a versão em texto simples (opcional)
    text_content = strip_tags(html_content)

    # 4. Criar a mensagem de e-mail usando EmailMultiAlternatives
    email = EmailMultiAlternatives(
        # Assunto
        assunto,
        # Conteúdo em texto simples
        text_content,
        # Remetente
        settings.EMAIL_HOST_USER,
        # Destinatários
        [destinatario],
    )

    # 5. Anexar a versão HTML
    email.attach_alternative(html_content, "text/html")

    # 6. Enviar o e-mail
    email.send()
