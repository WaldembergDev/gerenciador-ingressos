# configurações Whapi
import requests
from django.conf import settings
from django.http import JsonResponse

# configurações de email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# gerais
from requests.exceptions import HTTPError
import cloudscraper
from pprint import pprint


class Whapi:
    API_URL = "https://gate.whapi.cloud/"

    def __init__(self):
        self.token = settings.WHAPI_TOKEN

    def send_message_text(self, number: str, message: str):
        url = f"{self.API_URL}messages/text"

        payload = {"to": number, "body": message}

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.token}",
        }

        response = requests.post(url, json=payload, headers=headers)

        try:
            response.raise_for_status()
            dados = response.json()
            return JsonResponse(dados, status=201)
        except Exception as e:
            print(f"Erro: {e}")
            return None


class EmailService:
    def __init__(self):
        self.email_host_user = settings.EMAIL_HOST_USER

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
            self.email_host_user,
            # Destinatários
            [destinatario],
        )
        # 5. Anexar a versão HTML
        email.attach_alternative(html_content, "text/html")
        # 6. Enviar o e-mail
        email.send()

class ApiMaracaService:
    URL = 'https://api.maracana.rio.br/v1/bievents'

    def obter_proximos_jogos(self):
        scraper = cloudscraper.create_scraper()

        try:
            response = scraper.get(self.URL)
            response.raise_for_status()
            dados = response.json()
            return dados.get('res')
        except HTTPError as e:
            print(f'Erro de requisição: {e}')
        except Exception as e:
            print(f'Erro genérico: {e}')
