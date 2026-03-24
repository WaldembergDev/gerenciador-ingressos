import requests
from django.conf import settings
from datetime import date


class Asaas:
    # Constantes
    END_POINT = settings.ASAAS_END_POINT
    API_KEY = settings.ASAAS_API_KEY
    USER_AGENT = settings.ASAAS_USER_AGENT

    def criar_qr_code_pix_dinamico(self, id_cobranca: str):
        url = f"{self.END_POINT}/v3/payments/{id_cobranca}/pixQrCode"

        headers = {
            "User-Agent": self.USER_AGENT,
            "Content-Type": "application/json",
            "access_token": self.API_KEY,
        }

        params = {"id": id_cobranca}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            dados = response.json()
            encodedImage = dados.get("encodedImage")
            payload = dados.get("payload")
            validade = dados.get("expirationDate")
            description = dados.get("description")
            return (encodedImage, payload, validade, description)
        except Exception as e:
            print(f"Erro: {e}")

    def criar_cliente(self, name: str, cpf_cnpj: str):
        url = f"{self.END_POINT}/v3/customers"

        payload = {"name": name, "cpfCnpj": cpf_cnpj}

        headers = {
            "User-Agent": self.USER_AGENT,
            "Content-Type": "application/json",
            "access_token": self.API_KEY,
        }

        response = requests.post(url, json=payload, headers=headers)

        try:
            response.raise_for_status()
            dados = response.json()
            print("Cliente criado com sucesso!")
            return dados.get("id")
        except Exception as e:
            print(f"Erro: {e}")

    def listar_clientes(self, cpf_cnpj: str):
        url = f"{self.END_POINT}/v3/customers"

        params = {"cpfCnpj": cpf_cnpj}

        headers = {
            "User-Agent": self.USER_AGENT,
            "Content-Type": "application/json",
            "access_token": self.API_KEY,
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            dados = response.json()
            if dados.get("totalCount") > 1:
                raise ValueError(
                    "Foi encontrado mais de um cliente com o mesmo cpf/cnpj"
                )
            if dados.get("totalCount") < 1:
                raise ValueError("Não foi encontrado cliente com esse id")
            print("Cliente encontrado!")
            return dados.get("data")[0].get("id")
        except Exception as e:
            print(f"Erro: {e}")

    def criar_cobranca(
        self, id_cliente: str, forma_pagamento: str, valor: float, data_vencimento: date
    ):
        url = f"{self.END_POINT}/v3/payments"

        payload = {
            "customer": id_cliente,
            "billingType": forma_pagamento,
            "value": valor,
            "dueDate": data_vencimento,
        }

        headers = {
            "User-Agent": self.USER_AGENT,
            "Content-Type": "application/json",
            "access_token": self.API_KEY,
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            dados = response.json()
            return dados.get("id")
        except Exception as e:
            print(f"Erro: {e}")

    def criar_checkout(self, item: dict) -> tuple[str, str] | None:
        base_url = settings.BASE_URL.rstrip('/')
        url = f"{self.END_POINT}/v3/checkouts"

        payload = {
            "billingTypes": ["PIX"],
            "chargeTypes": ["DETACHED"],
            "minutesToExpire": 10,
            "callback": {
                "successUrl": f"{base_url}/pagamentos/sucesso/{item.get('id')}/",
                "cancelUrl": f"{base_url}/pagamentos/cancelado/",
            },
            "items": [
                {
                    "description": item.get("description"),
                    "imageBase64": item.get("imageBase64"),
                    "name": item.get("name"),
                    "quantity": item.get("quantity"),
                    "value": item.get("value"),
                }
            ],
        }

        headers = {
            "User-Agent": self.USER_AGENT,
            "Content-Type": "application/json",
            "access_token": self.API_KEY,
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            dados = response.json()
            id = dados.get("id")
            link = dados.get("link")
            return id, link
        except Exception as e:
            print(f"Erro: {e}")
            return None
