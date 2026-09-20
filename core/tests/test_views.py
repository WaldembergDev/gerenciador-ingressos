import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_acesso_inicial_senha_valida(client, acesso_geral_comum):
    url = reverse('acesso_inicial')

    formulario = {
        'senha': 'teste@123' 
    }

    response = client.post(url, data=formulario)

    assert response.status_code == 302

    url_destino = reverse('home')

    assert response['Location'] == url_destino

@pytest.mark.django_db
def test_acesso_inicial_status_code_302(client):
    url = reverse('acesso_inicial')

    sessao = client.session
    sessao['acesso_geral'] = 'teste@123'
    sessao.save()

    response = client.get(url)

    assert response.status_code == 302

    