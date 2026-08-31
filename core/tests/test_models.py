import pytest
from core.models import AcessoGeral
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

@pytest.mark.django_db
def test_acesso_geral():
    novo_acesso = AcessoGeral.objects.create(
        senha='senha_criptografada@'
    )

    assert novo_acesso.verificar_senha('senha_criptografada@')

@pytest.mark.django_db
def test_acesso_geral_limpeza_de_sessions():
    session = SessionStore()
    session['usuario_id'] = 1
    session.create()
    session_key = session.session_key

    # testa se a sessão foi criada
    assert session_key

    AcessoGeral.objects.create(
        senha='senha_criptografada@'
    )

    # testa se a sessão foi removida
    assert not Session.objects.all().exists()