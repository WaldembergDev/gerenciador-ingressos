from django.shortcuts import get_object_or_404, render, redirect
from .utils import Asaas
from django.http import HttpResponse
from datetime import date
from ingressos.models import HistoricoCompra
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.conf import settings



# Create your views here.
def criar_pagamento(request, id_historico_compra):
    # identificando o pedido
    pedido = get_object_or_404(HistoricoCompra, id=id_historico_compra)
    # instanciando a classe Asaas na variável
    asaas = Asaas()
    # criar cobrança
    vencimento_str = date.strftime(
        pedido.data_compra.date(), "%Y-%m-%d"
    )  # convertendo datetime para date
    cpf = pedido.cliente.cpf
    nome = pedido.cliente.usuario.first_name
    preco_str = str(pedido.valor_pago)
    cliente_id = asaas.listar_clientes(cpf)
    if not cliente_id:
        cliente_id = asaas.criar_cliente(nome, cpf)
    cobranca_id = asaas.criar_cobranca(cliente_id, "PIX", preco_str, vencimento_str)
    # atribuindo a cobrança gerada no asaas ao pedido
    pedido.id_cobranca_asaas = cobranca_id
    pedido.save()
    # gerando qr code
    dados = asaas.criar_qr_code_pix_dinamico(cobranca_id)
    if not dados:
        messages.error(request, "Erro ao gerar cobrança. Contate o administrador!")
        return redirect("comprar_ingresso", pedido.ingresso.id)

    context = {
        "qr_code": dados[0],
        "payload": dados[1],
        "validade": dados[2],
        "descricao": dados[3],
    }
    return render(request, "pagamentos/cobranca.html", context)


def criar_checkout(request, id_historico_compra):
    pedido = get_object_or_404(HistoricoCompra, id=id_historico_compra)
    item = {
        "description": pedido.titulo,
        "imageBase64": "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==",
        "name": pedido.titulo,
        "quantity": pedido.quantidade,
        "value": str(pedido.ingresso.preco),
    }

    asaas = Asaas()
    dados = asaas.criar_checkout(item)
    if dados is None:
        messages.error(request, 'Erro ao gerar cobrança')
        return redirect('comprar_ingresso', pedido.ingresso.id)
    id, link = dados
    pedido.id_checkout_asaas = id
    pedido.save()
    return redirect(link)


@csrf_exempt
def receber_webhook(request):
    auth_token = request.headers.get('asaas-access-token')
    if not auth_token == settings.ASAAS_TOKEN_WEBHOOK:
        return HttpResponse('Entrei onde não deveria')
        #return HttpResponse(content="Chave inválida!", status=403)
    data = json.loads(request.body)
    print(f"Webook recebido: {data}")
    event = data.get('event')
    id_checkout = data.get('checkout').get('id')
    pedido = get_object_or_404(HistoricoCompra, id_checkout_asaas=id_checkout)
    if event == 'CHECKOUT_EXPIRED' or event == 'CHECKOUT_CANCELED':
        pedido.status = HistoricoCompra.Status.CANCELADO
        pedido.ingresso.estoque_disponivel += 1
    elif event == 'CHECKOUT_PAID':
        pedido.status = HistoricoCompra.Status.APROVADO
    pedido.save()
    return HttpResponse(content="Tudo certo!", status=200)
