import pytest
from ingressos.models import HistoricoCompra, Ingresso
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils.timezone import make_aware
from django.db.models import ProtectedError

@pytest.mark.django_db
def test_ingresso_sem_vendas(ingresso_comum):    
    assert ingresso_comum.quantidade_vendido == 0

@pytest.mark.django_db
def test_ingresso_quantidade_vendido_apenas_compras_aprovadas(ingresso_comum, cliente_comum):

    def criar_historico(quantidade, status):
        HistoricoCompra.objects.create(
            cliente = cliente_comum,
            titulo = ingresso_comum.titulo,
            ingresso = ingresso_comum,
            local = ingresso_comum.local,
            data_horario_evento = ingresso_comum.data_horario,
            valor_pago = ingresso_comum.preco,
            quantidade = quantidade,
            status = status
        )

    criar_historico(1, HistoricoCompra.Status.APROVADO)
    criar_historico(1, HistoricoCompra.Status.APROVADO)
    criar_historico(3, HistoricoCompra.Status.PENDENTE)
    criar_historico(5, HistoricoCompra.Status.PENDENTE)

    assert ingresso_comum.quantidade_vendido == 2
    

@pytest.mark.django_db
def test_ingresso_estoque_inicial_calculo_correto(ingresso_comum, cliente_comum):
    historico = HistoricoCompra.objects.create(
        cliente = cliente_comum,
        titulo = ingresso_comum.titulo,
        ingresso = ingresso_comum,
        local = ingresso_comum.local,
        data_horario_evento = ingresso_comum.data_horario,
        valor_pago = ingresso_comum.preco,
        quantidade = 3,
        status = HistoricoCompra.Status.APROVADO
    )

    ingresso_comum.estoque_disponivel = ingresso_comum.estoque_disponivel - historico.quantidade
    ingresso_comum.save()

    assert ingresso_comum.quantidade_vendido == 3
    assert ingresso_comum.estoque_disponivel == 7
    assert ingresso_comum.estoque_inicial == 10

@pytest.mark.django_db
def test_ingresso_validacao_de_valor_minimo(ingresso_comum):
    with pytest.raises(ValidationError):
        ingresso_comum.preco = -50
        ingresso_comum.full_clean()

@pytest.mark.django_db
def test_ingresso_valores_padrao():
    data_evento = datetime(2026, 12, 1, 10, 0, 0)
    data_evento_django = make_aware(data_evento)

    ingresso = Ingresso.objects.create(
        tipo = Ingresso.TipoIngresso.SHOW,
        titulo = 'Evento Teste',
        local = 'Maracanã',
        descricao = 'Evento Teste',
        data_horario = data_evento_django,
        preco = 60.0,
    )

    assert ingresso.status == Ingresso.StatusIngresso.ATIVO
    assert ingresso.estoque_disponivel == 2

@pytest.mark.django_db
def test_representacao_em_texto(ingresso_comum, cliente_comum):
    historico = HistoricoCompra.objects.create(
                cliente = cliente_comum,
                titulo = ingresso_comum.titulo,
                ingresso = ingresso_comum,
                local = ingresso_comum.local,
                data_horario_evento = ingresso_comum.data_horario,
                valor_pago = ingresso_comum.preco,
                quantidade = 1,
                status = HistoricoCompra.Status.PENDENTE
            )
    
    assert str(ingresso_comum) == ingresso_comum.titulo
    assert str(historico) == f'{historico.data_compra:%d/%m/%Y %H:%M} - {historico.titulo} - {historico.id}'
    assert str(cliente_comum) == cliente_comum.usuario.first_name

@pytest.mark.django_db
def test_excluir_ingresso_vendido(ingresso_comum, cliente_comum):
    historico = HistoricoCompra.objects.create(
                    cliente = cliente_comum,
                    titulo = ingresso_comum.titulo,
                    ingresso = ingresso_comum,
                    local = ingresso_comum.local,
                    data_horario_evento = ingresso_comum.data_horario,
                    valor_pago = ingresso_comum.preco,
                    quantidade = 1,
                    status = HistoricoCompra.Status.PENDENTE
                )
    with pytest.raises(ProtectedError):
        ingresso_comum.delete()
