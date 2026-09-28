from django.core.management.base import BaseCommand
from django.conf import settings
import requests


class Command(BaseCommand):
    help = "Faz requisição na api do maracanã e atualiza o cache com os eventos futuros"

    def handle(self, *args, **options):
        url_maracana = 'https://api.maracana.rio.br/v1/bievents'
        url_sistema = 'https://ingressosmc.pythonanywhere.com/ingressos/eventos-webhook/'

        headers = {
            'X-Webhook-Token': getattr(settings, 'WEBHOOK_TOKEN', '')
        }
        
        response_maracana = requests.get(url_maracana)

        try:
            response_maracana.raise_for_status()
            # dados obtidos
            dados = response_maracana.json()
            # realizar requisição no sistema com os dados
            requests.post(
                url_sistema, json=dados, headers=headers
                )
        except Exception as e:
            print(f'Erro: {e}')
            # implementar envio de e-mail caso dê erro