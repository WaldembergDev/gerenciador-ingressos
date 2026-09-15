import pytest
from ingressos.forms import CompraForm, IngressoForm, VendaRapidaForm
from times.models import Time
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
from django.utils import timezone


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


@pytest.mark.django_db
def test_ingresso_form_valido():
    # criando os times
    pixel_gif = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    
    escudo = SimpleUploadedFile(
        name="teste.gif", 
        content=pixel_gif, 
        content_type="image/gif"
    )

    time_casa = Time.objects.create(
        nome='Time A',
        escudo=escudo
    )

    time_visitante = Time.objects.create(
        nome='Time B',
        escudo=escudo
    )

    # obtendo os dados para o formulário
    dados = {
        'time_casa': time_casa.id,
        'time_visitante': time_visitante.id,
        'titulo': 'Time A VS Time B',
        'tipo': 'JOGO',
        'local': 'Maracanã',
        'descricao': 'Ala Vip',
        'data_horario': timezone.make_aware(datetime(2026, 10, 1, 10, 30)),
        'preco': 60.0,
        'estoque_disponivel': 2,
        'status': 'ATIVO'
    }

    form = IngressoForm(data=dados)

    assert form.is_valid() is True

@pytest.mark.django_db
def test_ingresso_form_invalido_times_iguais():
    # criando os times
    pixel_gif = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    
    escudo = SimpleUploadedFile(
        name="teste.gif", 
        content=pixel_gif, 
        content_type="image/gif"
    )

    time_casa = Time.objects.create(
        nome='Time A',
        escudo=escudo
    )

    # obtendo os dados para o formulário
    dados = {
        'time_casa': time_casa.id,
        'time_visitante': time_casa.id,
        'titulo': 'Time A VS Time B',
        'tipo': 'JOGO',
        'local': 'Maracanã',
        'descricao': 'Ala Vip',
        'data_horario': timezone.make_aware(datetime(2026, 10, 1, 10, 30)),
        'preco': 60.0,
        'estoque_disponivel': 2,
        'status': 'ATIVO'
    }

    form = IngressoForm(data=dados)

    assert form.is_valid() is False


@pytest.mark.django_db
def test_venda_form_valido(cliente_comum, ingresso_comum):
    dados = {
        'cliente': cliente_comum.id,
        'ingresso': ingresso_comum.id,
        'quantidade': 2,
        'status': 'P'
    }

    form = VendaRapidaForm(data=dados)

    assert form.is_valid() is True


@pytest.mark.django_db
def test_venda_form_invalido(cliente_comum, ingresso_comum):
    dados = {
        'cliente': cliente_comum.id,
        'ingresso': ingresso_comum.id,
        'quantidade': -2,
        'status': 'P'
    }

    form = VendaRapidaForm(data=dados)

    assert form.is_valid() is False