import pytest
from ingressos.forms import CompraForm


@pytest.mark.django_db
def test_compra_form_valido(ingresso_comum):
    dados = {
        'quantidade': 2
    }
    form = CompraForm(data=dados, ingresso=ingresso_comum)
    assert form.is_valid() is True


@pytest.mark.django_db
def test_compra_form_invalido(ingresso_comum):
    dados = {
        'quantidade': 12
    }
    form = CompraForm(data=dados, ingresso=ingresso_comum)
    assert form.is_valid() is False