import pytest
from ingressos.models import Ingresso, HistoricoCompra
from clientes.models import Cliente, Endereco
from core.models import CustomUser
from datetime import datetime, date
from django.utils import timezone

@pytest.fixture
def ingresso_comum(db):
    data_comum = datetime(2026, 12, 1, 10, 0, 0)
    data_django = timezone.make_aware(data_comum)
    ingresso = Ingresso.objects.create(
        tipo = Ingresso.TipoIngresso.SHOW,
        titulo = "Evento Teste",
        local = 'Maracanã',
        descricao = 'Cadeira Cativa',
        data_horario = data_django,
        preco = 50.00,
        preco_par = 70.00,
        estoque_disponivel = 10
    )
    return ingresso

@pytest.fixture
def cliente_comum(db):
    usuario = CustomUser.objects.create_user(
        first_name = 'Waldemberg',
        last_name = 'Pereira',
        username = 'usuario',
        email = 'teste@gmail.com'
    )
    cliente = Cliente.objects.create(
        telefone = '21974005040',
        data_nascimento = date(1993, 9, 30),
        usuario = usuario
    )
    return cliente

@pytest.fixture
def historico_comum(db, cliente_comum, ingresso_comum):
    historico = HistoricoCompra.objects.create(
        cliente = cliente_comum,
        ingresso = ingresso_comum,
        titulo = ingresso_comum.titulo,
        local = ingresso_comum.local,
        data_horario_evento = ingresso_comum.data_horario,
        valor_pago = ingresso_comum.preco,
        quantidade = 1,
        status = HistoricoCompra.Status.APROVADO
    )
    return historico

@pytest.fixture
def endereco_comum(db, cliente_comum):
    endereco = Endereco.objects.create(
        cep = '21250610',
        logradouro = 'Rua Andrade',
        numero = '100',
        bairro = 'Andrade',
        cidade = 'Rio de Janeiro',
        estado = 'Rio de Janeiro',
        uf = Endereco.UfEnum.RIO_DE_JANEIRO,
        cliente = cliente_comum
    )
    return endereco