import pytest
from clientes.forms import ClienteForm
from datetime import date

@pytest.mark.django_db
def test_cliente_form_valido(usuario_comum):
    dados = {
        'telefone': '21974000000',
        'data_nascimento': '1993-09-30',
        'rg': '27024266-5',
        'cpf': '10999319746',
        'sexo': 'M',
    }

    form = ClienteForm(data=dados)
    assert form.is_valid()

    cliente = form.save(commit=False)
    cliente.usuario = usuario_comum
    cliente.save()

    assert cliente.telefone == '21974000000'
    assert cliente.pk is not None

@pytest.mark.django_db
def test_cliente_form_invalido():
    dados = {
        'telefone': '21974000000',
        'data_nascimento': '1993-09-30',
        'rg': '27024266-5',
        'cpf': '10999319746',
        'sexo': 'B',
    }
    form = ClienteForm(data=dados)
    assert not form.is_valid()
    assert 'sexo' in form.errors
