import requests
from django.conf import settings
from django.http import JsonResponse


class Whapi:

    API_URL = 'https://gate.whapi.cloud/'

    def __init__(self):
        self.token = settings.WHAPI_TOKEN
    
    def send_message_text(self, number: str, message: str):
        url = f'{self.API_URL}messages/text'

        payload = {
            'to': number,
            'body': message   
        }

        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'authorization': f'Bearer {self.token}'
        }

        response = requests.post(url, json=payload, headers=headers)

        try:
            response.raise_for_status()
            dados = response.json()
            return JsonResponse(dados, status=201)
        except Exception as e:
            print(f'Erro: {e}')
            return None
        
        