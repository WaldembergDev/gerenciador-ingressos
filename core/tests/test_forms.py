import pytest
from core.forms import (
    AcessoGeralForm,
    AcessoGeralFormCreate,
    CustomUserForm,
    CustomUserUpdateForm,
    CustomUserUpdateFormAdmin,
    EmailAuthenticationForm,
    ResetSenhaForm,
)
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_form_autenticacao_valido():
    User.objects.create_user(
        username="teste@gmail.com", email="teste@gmail.com", password="@1234@456@"
    )
    data = {
        "username": "teste@gmail.com",
        "password": "@1234@456@",
    }
    form = EmailAuthenticationForm(data=data)

    assert form.is_valid()


@pytest.mark.django_db
def test_form_autenticacao_invalido():
    User.objects.create_user(
        username="teste@gmail.com", email="teste@gmail.com", password="@1234@456@"
    )
    data = {
        "username": "teste@gmail.com",
        "password": "12345678",
    }
    form = EmailAuthenticationForm(data=data)

    assert not form.is_valid()


@pytest.mark.django_db
def test_form_custom_user_valido():
    dados = {
        "email": "teste@gmail.com",
        "password": "@123@456",
        "password2": "@123@456",
        "first_name": "usuario_first_name",
        "last_name": "usuario_last_name",
        "autoriza_notificacoes": True,
    }

    form = CustomUserForm(data=dados)

    assert form.is_valid()
    # salva o usuário
    usuario = form.save(commit=False)

    assert usuario.email == "teste@gmail.com"
    assert usuario.first_name == "usuario_first_name"


@pytest.mark.django_db
def test_form_custom_user_invalido():
    dados = {
        "email": "teste@gmail.com",
        "password": "@123@456",
        "password2": "123456",
        "first_name": "usuario_first_name",
        "last_name": "usuario_last_name",
        "autoriza_notificacoes": True,
    }

    form = CustomUserForm(data=dados)

    assert not form.is_valid()


@pytest.mark.django_db
def test_acesso_geral_form_valido():
    dados = {"senha": "teste@123"}
    form = AcessoGeralForm(data=dados)

    assert form.is_valid()


@pytest.mark.django_db
def test_acesso_geral_form_invalido():
    dados = {"senha": ""}
    form = AcessoGeralForm(data=dados)

    assert not form.is_valid()


@pytest.mark.django_db
def test_acesso_geral_form_create_valido():
    dados = {"senha": "teste@123", "confirmacao_password": "teste@123"}
    form = AcessoGeralFormCreate(data=dados)

    assert form.is_valid()


@pytest.mark.django_db
def test_acesso_geral_form_create_invalido():
    dados = {"senha": "teste@123", "confirmacao_password": "teste@abc"}
    form = AcessoGeralFormCreate(data=dados)

    assert not form.is_valid()


@pytest.mark.django_db
def test_custom_user_update_form_admin_valido(usuario_comum):
    dados = {
        "first_name": "usuario_first_name",
        "last_name": "usuario_last_name",
        "email": "novo_email@gmail.com",
        "is_active": False,
        "autoriza_notificacoes": False,
    }
    form = CustomUserUpdateFormAdmin(data=dados, instance=usuario_comum)

    assert form.is_valid()

    form.save()

    assert usuario_comum.first_name == "usuario_first_name"
    assert usuario_comum.is_active == False


@pytest.mark.django_db
def test_custom_user_update_form_admin_invalido(usuario_comum):
    dados = {
        "first_name": "usuario_first_name",
        "last_name": "usuario_last_name",
        "autoriza_notificacoes": False,
    }
    form = CustomUserUpdateFormAdmin(data=dados, instance=usuario_comum)

    assert not form.is_valid()


@pytest.mark.django_db
def test_custom_user_update_form_valido(usuario_comum):
    dados = {
        "first_name": "usuario_first_name",
        "last_name": "usuario_last_name",
        "email": "novo_email@gmail.com",
    }
    form = CustomUserUpdateForm(data=dados, instance=usuario_comum)

    assert form.is_valid()

    assert usuario_comum.email == "novo_email@gmail.com"


@pytest.mark.django_db
def test_custom_user_update_form_invalido():
    dados = {
        "first_name": "usuario_first_name",
        "last_name": "usuario_last_name",
        "email": "",
    }
    form = CustomUserUpdateForm(data=dados)

    assert not form.is_valid()


@pytest.mark.django_db
def test_reset_senha_form_valido(usuario_comum):
    dados = {
        'password': 'novo_password',
        'confirmacao_password': 'novo_password'
    }
    form = ResetSenhaForm(data=dados)
    assert form.is_valid()


@pytest.mark.django_db
def test_reset_senha_form_invalido():
    dados = {
        'password': 'novo_password',
        'confirmacao_password': 'senha_diferente'
    }
    form = ResetSenhaForm(data=dados)
    assert not form.is_valid()