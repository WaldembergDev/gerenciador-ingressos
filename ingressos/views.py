from email import message
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction, models
from django.urls import reverse

from core.models import CustomUser
from .models import Ingresso, HistoricoCompra
from django.shortcuts import get_object_or_404
from .forms import CompraForm, IngressoForm
from django.contrib import messages
from clientes.models import Cliente

from django.contrib.auth.decorators import login_required

@login_required
def comprar_ingresso(request, id_ingresso):
    ingresso = get_object_or_404(Ingresso, pk=id_ingresso)
    if not request.user.is_authenticated:
        url_final = f"{reverse('core_login')}?next={request.path}"
        return redirect(url_final)
    if request.method == 'POST':
        form = CompraForm(request.POST, ingresso=ingresso)
        if form.is_valid():
            # if request.user.is_admin:
            #     messages.error(request, 'Administrador, faz sentido você comprar ingresso?')
            #     return redirect('comprar_ingresso', ingresso.id)
            try:                
                with transaction.atomic():
                    quantidade = form.cleaned_data['quantidade']
                    ingresso_travado = Ingresso.objects.select_for_update().get(pk=id_ingresso)
                    if quantidade > ingresso_travado.estoque_disponivel:
                        raise Exception('Estoque insuficiente para esta compra.')
                    ingresso_travado.estoque_disponivel -= quantidade
                    ingresso_travado.save()

                    # obtendo o usuário logado
                    usuario = request.user
                    # obtendo o perfil de cliente do usuário logado
                    cliente = Cliente.objects.get(usuario=usuario)
        
                    HistoricoCompra.objects.create(
                        cliente=cliente,
                        ingresso=ingresso_travado,
                        titulo=ingresso_travado.titulo,
                        local=ingresso_travado.local,
                        valor_pago=ingresso_travado.preco,
                        quantidade=quantidade,
                        data_horario_evento=ingresso_travado.data_horario
                        )
                    messages.success(request, 'Obrigado! Seu ingresso foi comprado com sucesso! Aguarde o contato do administrador')
                    return redirect('home')
            except Exception as e:
                messages.error(request, e)
                return redirect('comprar_ingresso', ingresso.id)
    else:
        form = CompraForm()
    context = {
        'form': form,
        'ingresso': ingresso
    }
    return render(request, 'ingressos/comprar_ingresso.html', context=context)

@login_required
def visualizar_ingresso(request, id_ingresso):
    ingresso = get_object_or_404(Ingresso, pk=id_ingresso)
    if request.method == 'POST':
        pass
    else:
        context = {'ingresso': ingresso}
    return render(request, '')

@login_required
def cadastrar_ingresso(request):
    if request.method == 'POST':
        form = IngressoForm(request.POST, request.FILES, esconder_campo=True)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingresso cadastrado com sucesso!')
            return redirect('cadastrar_ingresso')
    else:
        form = IngressoForm()
    context = {
        'form': form
    }
    return render(request, 'ingressos/cadastrar_ingresso.html', context=context)

@login_required
def exibir_todos_ingressos_comprados(request):
    ingressos_comprados = HistoricoCompra.objects.all()
    context = {
        'ingressos_comprados': ingressos_comprados
    }
    return render(request, 'ingressos/todos_ingressos_comprados.html', context=context)

@login_required
def exibir_meus_ingressos(request):
    # if request.user.is_admin:
    #         messages.error(request, 'Administrador, faz sentido você visualizar seus ingressos comprados?')
    #         return redirect('home')
    usuario = request.user
    cliente = Cliente.objects.get(usuario=usuario)
    compras = HistoricoCompra.objects.filter(cliente=cliente).order_by('data_horario_evento')
    context = {
        'compras': compras
    }
    return render(request, 'ingressos/meus_ingressos.html', context=context)

@login_required
def json_detalhes_compra(request, id_historico):
    detalhes = get_object_or_404(HistoricoCompra, id=id_historico)
    dados = {
        'titulo': detalhes.titulo,
        'local': detalhes.local,
        'data_compra': detalhes.data_compra,
        'valor_pago': detalhes.valor_pago,
        'quantidade': detalhes.quantidade
    }
    return JsonResponse(dados)

@login_required
def editar_ingresso(request, id_ingresso):
    ingresso = get_object_or_404(Ingresso, id=id_ingresso)
    if request.method == 'POST':
        form = IngressoForm(request.POST, request.FILES, instance=ingresso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados salvos com sucesso!')
            return redirect('editar_ingresso', ingresso.id)
    else:
        form = IngressoForm(instance=ingresso)
    context = {
        'form': form,
        'ingresso': ingresso
    }
    return render(request, 'ingressos/editar_ingresso.html', context=context)
    