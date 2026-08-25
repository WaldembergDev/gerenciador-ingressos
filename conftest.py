import pytest
from ingressos.models import Ingresso, HistoricoCompra
from clientes.models import Cliente, Endereco
from times.models import Time
from core.models import CustomUser
from datetime import datetime, date
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

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
def usuario_comum(db):
    usuario = CustomUser.objects.create_user(
        first_name = 'Waldemberg',
        last_name = 'Pereira',
        username = 'usuario',
        email = 'teste@gmail.com'
    )
    return usuario

@pytest.fixture
def cliente_comum(db, usuario_comum):
    cliente = Cliente.objects.create(
        telefone = '21974005040',
        data_nascimento = date(1993, 9, 30),
        usuario = usuario_comum
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

@pytest.fixture
def time_comum(db):
    conteudo_imagem = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff'
        b'\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00'
        b'\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    )

    escudo_fake = SimpleUploadedFile(
        name = 'teste.gif',
        content = conteudo_imagem,
        content_type = 'image/gif'
    )
    time = Time.objects.create(
        nome = 'Flamengo',
        escudo = escudo_fake
    )

    return time