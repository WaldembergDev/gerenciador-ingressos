import pytest
from django.urls import reverse
from clientes.models import Cliente
from datetime import date
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_view_criar_conta_cliente_valida(client, acesso_geral_comum):
    sessao = client.session
    sessao['acesso_geral'] = 'teste@123'
    sessao.save()

    url = reverse('criar-conta-cliente')

    dados_formulario = {
        # dados cliente
        'telefone': '21974000000',
        'data_nascimento': date(1993, 1, 1),
        'rg': '123456',
        'cpf': '123456',
        'sexo': 'M',
        # dados usuário
        'email': 'teste@gmail.com',
        'password': 'Senha@123',
        'password2': 'Senha@123',
        'first_name': 'Primeiro_Nome',
        'last_name': 'Ultimo_nome',
        'autoriza_notificacoes': True
    }

    response = client.post(url, data=dados_formulario)

    assert response.status_code == 302
    assert Cliente.objects.filter(telefone='21974000000').exists()

@pytest.mark.django_db
def test_client_list(client, acesso_geral_comum):
    # criando o usuário
    usuario = User.objects.create_superuser(
        password='teste@123',
        first_name='Primeiro_Nome',
        last_name='Segundo_Nome',
        email='teste@gmail.com'
    ) # type: ignore

    # criando a sessão de acesso_geral
    sessao = client.session
    sessao['acesso_geral'] = 'teste@123'
    sessao.save()

    client.force_login(usuario)

    url = reverse('cliente_list')

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_toggle_cliente_status(client, acesso_geral_comum, cliente_comum):
    # criando o usuário
    usuario = User.objects.create_superuser(
        password='teste@123',
        first_name='Primeiro_Nome',
        last_name='Segundo_Nome',
        email='teste123@gmail.com'
    ) # type: ignore

    sessao = client.session
    sessao['acesso_geral'] = 'teste@123'
    sessao.save()

    client.force_login(usuario)

    url = reverse('toggle_cliente_status', args=[cliente_comum.id])
    response = client.post(url)
    assert response.status_code == 302

    # recarrega o objeto do banco de dados para pegar as alterações salvas pela view
    cliente_comum.usuario.refresh_from_db()
    assert cliente_comum.usuario.is_active is False

@pytest.mark.django_db
def test_cliente_detail_view(client, cliente_comum):
    # criando o usuário
    usuario = User.objects.create_superuser(
        password='teste@123',
        first_name='Primeiro_Nome',
        last_name='Segundo_Nome',
        email='teste123@gmail.com'
    ) # type: ignore

    sessao = client.session
    sessao['acesso_geral'] = 'teste@123'
    sessao.save()

    client.force_login(usuario)

    url = reverse('cliente_detail', args=[cliente_comum.id])

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_cliente_detail_edit(client, cliente_comum):
    # criando o usuário
    usuario = User.objects.create_superuser(
        password='teste@123',
        first_name='Primeiro_Nome',
        last_name='Segundo_Nome',
        email='teste123@gmail.com'
    ) # type: ignore

    sessao = client.session
    sessao['acesso_geral'] = 'teste@123'
    sessao.save()

    client.force_login(usuario)

    url = reverse('cliente_detail', args=[cliente_comum.id])

    dados_formulario = {
        # dados do cliente
        'telefone': '2197400000000',
        'data_nascimento': date(1993, 1, 1),
        'rg': '123456',
        'cpf': '123456789',
        'sexo': 'M',
        # dados do user
        'first_name': 'Primeiro_Nome',
        'last_name': 'Ultimo_Nome',
        'email': 'teste1234@gmail.com',
        'autoriza_notificacoes': True
    }

    response = client.post(url, data=dados_formulario)

    assert response.status_code == 302

    # verifica se foi atualizado os dados do cliente
    cliente_comum.refresh_from_db()
    assert cliente_comum.cpf == '123456789'


@pytest.mark.django_db
def test_admin_create_client(client):
    # criando o usuário
    usuario = User.objects.create_superuser(
        password='teste@123',
        first_name='Primeiro_Nome',
        last_name='Segundo_Nome',
        email='teste123@gmail.com'
    ) # type: ignore

    sessao = client.session
    sessao['acesso_geral'] = 'teste@123'
    sessao.save()

    client.force_login(usuario)

    url = reverse('admin_create_client')

    dados_formulario = {
        # dados do cliente
        'telefone': '2197400000000',
        'data_nascimento': date(1993, 1, 1),
        'rg': '1230147',
        'cpf': '123456789',
        'sexo': 'M',
        # dados do user
        'first_name': 'Primeiro_Nome',
        'last_name': 'Ultimo_Nome',
        'email': 'teste1234@gmail.com',
        'autoriza_notificacoes': True,
        'password': 'teste@123',
        'password2': 'teste@123',
    }

    response = client.post(url, data=dados_formulario)

    assert response.status_code == 302
    # verifica se foi criado o usuário no banco de dados
    assert Cliente.objects.filter(rg='1230147').exists()