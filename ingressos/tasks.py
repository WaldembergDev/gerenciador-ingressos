import requests
from decouple import config
from celery import shared_task
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task(name='notificacao_compra_whatsapp', bind=True, max_retries=3)
def enviar_notificacao(self, numero:str, evento: str, data_evento: str):
    url = 'https://graph.facebook.com/v22.0/964251236763798/messages'
    token = settings.TOKEN_WHATSAPP

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": numero,
        "type": "template",
        "template": {
            "name": "notificacao_compra",
            "language": {
            "code": "pt_BR"
            },
            "components": [
            # <!-- Only required if the template uses body component parameters -->
            {
                "type": "body",
                "parameters": [
                {
                    "type": "text",
                    "parameter_name": "evento",
                    "text": evento
                },
                {
                    "type": "text",
                    "parameter_name": "data",
                    "text": data_evento
                },
                
                # <!-- Additional parameters values would follow, if needed -->

                ]
            }
            ]
        }
        }

    response = requests.post(url, headers=headers, json=data)

    try:
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Falha ao enviar notificação: {e}")
        raise self.retry(countdown=60)


def obter_proximos_eventos():
    pass
# https://api.maracana.rio.br/v1/bievents
