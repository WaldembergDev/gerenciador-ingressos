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


@pytest.mark.django_db
def test_home(client, ingresso_comum):
    url = reverse('home')

    sessao = client.session
    sessao['acesso_geral'] = 'teste@123'
    sessao.save()

    response = client.get(url)

    assert response.status_code == 200

    assert ingresso_comum in response.context['ingressos']


@pytest.mark.django_db
def test_login(client, cliente_comum):
    url = reverse('core_login')

    session = client.session
    session['acesso_geral'] = 'teste@123'
    session.save()

    formulario_login = {
        'username': 'teste@gmail.com',
        'password': '@1234@456@'
    }

    response = client.post(url, data=formulario_login)

    assert response.status_code == 302

    assert response['Location'] == reverse('home')


@pytest.mark.django_db
def test_login_senha_errada(client, cliente_comum):
    url = reverse('core_login')

    session = client.session
    session['acesso_geral'] = 'teste@123'
    session.save()

    formulario_login = {
        'username': 'teste@gmail.com',
        'password': '123456'
    }

    response = client.post(url, data=formulario_login)

    form_errors = response.context['form'].errors

    assert 'password' in form_errors or '__all__' in form_errors

@pytest.mark.django_db
def test_login_autenticado(client, usuario_comum):
    url = reverse('core_login')

    session = client.session
    session['acesso_geral'] = 'teste@123'
    session.save()

    client.force_login(usuario_comum)

    response = client.get(url)

    assert response.status_code == 302

    assert response['Location'] == reverse('home')
    