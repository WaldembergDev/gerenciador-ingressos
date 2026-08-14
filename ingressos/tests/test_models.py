import pytest
from ingressos.models import HistoricoCompra

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
