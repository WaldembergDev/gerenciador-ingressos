import datetime

from django.shortcuts import get_object_or_404, render
from .utils import Asaas
from django.http import HttpResponse
from datetime import date, timedelta
from ingressos.models import HistoricoCompra

# Create your views here.
def criar_pagamento(request, id_historico_compra):
    # identificando o pedido
    pedido = get_object_or_404(HistoricoCompra, id=id_historico_compra)
    # instanciando a classe Asaas na variável
    asaas = Asaas()
    # criar cobrança
    data = pedido.data_compra.date() # convertendo datetime para date
    vencimento = data + timedelta(days=1)
    cpf = pedido.cliente.cpf
    nome = pedido.cliente.usuario.first_name
    preco = pedido.valor_pago
    cliente_id = asaas.listar_clientes(cpf)
    if not cliente_id:
        cliente_id = asaas.criar_cliente(nome, cpf)
    cobranca_id = asaas.criar_cobranca(cliente_id, 'PIX', str(preco), date.strftime(vencimento, '%Y-%m-%d'))
    # atribuindo a cobrança gerada no asaas ao pedido
    pedido.id_cobranca_asaas = cobranca_id
    pedido.save()
    # gerando qr code
    dados = asaas.criar_qr_code_pix_dinamico(cobranca_id)

    context = {
        'qr_code': dados[0],
        'payload': dados[1],
        'validade': dados[2],
        'descricao': dados[3]
    }
    return render(request, 'pagamentos/cobranca.html', context)