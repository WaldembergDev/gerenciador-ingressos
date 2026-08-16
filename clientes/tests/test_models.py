import pytest

@pytest.mark.django_db
def test_status_cliente_novo(cliente_comum):
    assert cliente_comum.obter_status == 'Ativo'

@pytest.mark.django_db
def test_status_cliente_inativo(cliente_comum):
    cliente_comum.usuario.is_active = False
    cliente_comum.usuario.save()
    assert cliente_comum.obter_status == 'Inativo'

@pytest.mark.django_db
def test_cliente_novo_quantidade_comprada(cliente_comum):
    assert cliente_comum.obter_pedidos_aprovados == 0

@pytest.mark.django_db
def test_pedidos_aprovados(cliente_comum, historico_comum):
    assert cliente_comum.obter_pedidos_aprovados == 1

@pytest.mark.django_db
def test_representacao_texto(cliente_comum, endereco_comum):
    assert str(cliente_comum) == cliente_comum.usuario.first_name
    assert str(endereco_comum) == 'Rua Andrade'