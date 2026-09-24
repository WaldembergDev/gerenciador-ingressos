import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


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


@pytest.mark.django_db
def test_admin_resetar_senha_usuario(client, cliente_comum):
    usuario = cliente_comum.usuario
    usuario_admin = User.objects.create_superuser(
        username='usuario_admin@gmail.com',
        email='usuario_admin@gmail.com',
        password='teste@123'
    )

    url = reverse('admin_resetar_senha_usuario', kwargs={'id_usuario': usuario.id})

    session = client.session
    session['acesso_geral'] = 'teste@123'
    session.save()

    client.force_login(usuario_admin)

    response = client.post(url)

    assert response.status_code == 302

    # atualiza o objecto com os novos dados do banco
    usuario.refresh_from_db()
    # verifica se a senha foi alterada
    assert usuario.check_password('12345678')


@pytest.mark.django_db
def test_view_minha_conta_modo_get(client, usuario_comum):
    url = reverse('minha-conta')

    session = client.session
    session['acesso_geral'] = 'teste@123'
    session.save()

    client.force_login(usuario_comum)    
    
    response = client.get(url)

    assert response.status_code == 200

    # obtém o formulário enviado para o template
    form = response.context['form_custom_user']

    assert form.instance.first_name == 'Waldemberg'


@pytest.mark.django_db
def test_view_minha_conta_atualizacao(client, usuario_comum, cliente_comum):
    url = reverse('minha-conta')

    session = client.session
    session['acesso_geral'] = 'teste@123'
    session.save()

    client.force_login(usuario_comum)

    formulario = {
        # novos dados para o usuário
        'first_name': 'Pedro',
        'last_name': 'Teste',
        'email': 'teste_atualizacao@gmail.com',
        'autoriza_notificacoes': True,
        'telefone': cliente_comum.telefone,
        'data_nascimento': cliente_comum.data_nascimento,
    }

    response = client.post(url, data=formulario)

    assert response.status_code == 302

    usuario_comum.refresh_from_db()

    assert usuario_comum.first_name == 'Pedro'


@pytest.mark.django_db
def test_reset_senha(client, usuario_comum, cliente_comum):
    url = reverse('reset_senha')

    session = client.session
    session['acesso_geral'] = 'teste@123'
    session.save()

    client.force_login(usuario_comum)

    formulario = {
        'password': '@teste123',
        'confirmacao_password': '@teste123'
    }

    response = client.post(url, data=formulario)

    assert response.status_code == 302

    usuario_comum.refresh_from_db()

    assert usuario_comum.check_password('@teste123')


 