from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.urls import reverse
from .models import Ingresso, HistoricoCompra
from .forms import CompraForm, IngressoForm, VendaRapidaForm
from django.contrib import messages
from clientes.models import Cliente
from django.core.paginator import Paginator
from datetime import datetime
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from core.utils import superuser_check
from integracoes.services import ApiMaracaService
from django.core.cache import cache
from django.utils import timezone
import json


@login_required
def comprar_ingresso(request, id_ingresso):
    ingresso = get_object_or_404(Ingresso, pk=id_ingresso)
    if not request.user.is_authenticated:
        url_final = f"{reverse('core_login')}?next={request.path}"
        return redirect(url_final)
    if request.method == "POST":
        form = CompraForm(request.POST, ingresso=ingresso)
        if form.is_valid():
            if request.user.is_admin:
                messages.error(
                    request,
                    "Você está logado como administrador. Para testar compras, use uma conta de cliente",
                )
                return redirect("comprar_ingresso", ingresso.id)
            try:
                with transaction.atomic():
                    quantidade = form.cleaned_data["quantidade"]
                    ingresso_travado = Ingresso.objects.select_for_update().get(
                        pk=id_ingresso
                    )
                    if quantidade > ingresso_travado.estoque_disponivel:
                        raise Exception("Estoque insuficiente para esta compra.")
                    ingresso_travado.estoque_disponivel -= quantidade
                    ingresso_travado.save()

                    # obtendo o usuário logado
                    usuario = request.user
                    # obtendo o perfil de cliente do usuário logado
                    cliente = Cliente.objects.get(usuario=usuario)

                    historico = HistoricoCompra.objects.create(
                        cliente=cliente,
                        ingresso=ingresso_travado,
                        titulo=ingresso_travado.titulo,
                        local=ingresso_travado.local,
                        valor_pago=ingresso_travado.preco * quantidade,
                        quantidade=quantidade,
                        data_horario_evento=ingresso_travado.data_horario,
                    )
                    return redirect("criar_pagamento", id_historico_compra=historico.id)
            except Exception as e:
                messages.error(request, e)
                return redirect("comprar_ingresso", ingresso.id)
    else:
        form = CompraForm()
    context = {"form": form, "ingresso": ingresso}
    return render(request, "ingressos/comprar_ingresso.html", context=context)


@login_required
def exibir_meus_ingressos(request):
    if request.user.is_admin:
        messages.error(
            request,
            "Você está logado como administrador. Para visualizar seus ingressos comprados, logue como cliente.",
        )
        return redirect("home")
    usuario = request.user
    cliente = Cliente.objects.get(usuario=usuario)
    compras = HistoricoCompra.objects.filter(cliente=cliente).order_by(
        "data_horario_evento"
    )
    paginator = Paginator(compras, 20)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}

    return render(request, "ingressos/meus_ingressos.html", context=context)


@login_required
def json_detalhes_compra(request, id_historico):
    detalhes = get_object_or_404(
        HistoricoCompra, id=id_historico, cliente__usuario=request.user
    )
    dados = {
        "titulo": detalhes.titulo,
        "local": detalhes.local,
        "data_compra": detalhes.data_compra,
        "valor_pago": detalhes.valor_pago,
        "quantidade": detalhes.quantidade,
    }
    return JsonResponse(dados)


@login_required
@user_passes_test(superuser_check)
def cadastrar_ingresso(request):
    if request.method == "POST":
        form = IngressoForm(request.POST, request.FILES, esconder_campo=True)
        if form.is_valid():
            form.save()
            messages.success(request, "Ingresso cadastrado com sucesso!")
            return redirect("cadastrar_ingresso")
    else:
        form = IngressoForm()
    context = {"form": form}
    return render(request, "ingressos/cadastrar_ingresso.html", context=context)


@login_required
@user_passes_test(superuser_check)
def exibir_todos_ingressos_comprados(request):
    # obtendo os ingressos comprados
    ingressos_comprados = HistoricoCompra.objects.order_by("data_horario_evento")
    # aplicando filtro
    filtros = {}
    comprador = request.GET.get("comprador")
    evento = request.GET.get("evento")
    data_evento_str = request.GET.get("dataEvento")

    if comprador:
        filtros["cliente__usuario__first_name__icontains"] = comprador

    if evento:
        filtros["titulo__icontains"] = evento

    if data_evento_str:
        data_evento = datetime.strptime(data_evento_str, "%Y-%m-%d").date()
        filtros["data_horario_evento__date"] = data_evento

    if filtros:
        ingressos_comprados = ingressos_comprados.filter(**filtros)

    # configurando o paginator (30 itens por página)
    paginator = Paginator(ingressos_comprados, 30)
    # capturando o número da página atual
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, "ingressos/todos_ingressos_comprados.html", context=context)


@login_required
@user_passes_test(superuser_check)
def editar_ingresso(request, id_ingresso):
    ingresso = get_object_or_404(Ingresso, id=id_ingresso)
    if request.method == "POST":
        form = IngressoForm(request.POST, request.FILES, instance=ingresso)
        if form.is_valid():
            form.save()
            messages.success(request, "Dados salvos com sucesso!")
            return redirect("ingresso_list")
    else:
        form = IngressoForm(instance=ingresso)
    context = {"form": form, "ingresso": ingresso}
    return render(request, "ingressos/editar_ingresso.html", context=context)


@login_required
@user_passes_test(superuser_check)
def historico_venda_detail(request, id_historico):
    historico = get_object_or_404(HistoricoCompra, id=id_historico)
    context = {"historico": historico}
    return render(request, "ingressos/historico_compra_detail.html", context)


@login_required
@user_passes_test(superuser_check)
def ingresso_list(request):
    ingressos = Ingresso.objects.all().order_by("data_horario")

    paginator = Paginator(ingressos, 30)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, "ingressos/ingresso_list.html", context)


@login_required
@user_passes_test(superuser_check)
@require_POST
def ingresso_delete(request, id_ingresso):
    ingresso = get_object_or_404(Ingresso, id=id_ingresso)
    if ingresso.quantidade_vendido > 0:
        messages.error(
            request,
            "Não é possível excluir o ingresso, pois já existem ingressos vendidos",
        )
        return redirect("ingresso_list")
    ingresso.delete()
    messages.success(request, "Ingresso excluído com sucesso!")
    return redirect("ingresso_list")


@login_required
@user_passes_test(superuser_check)
def venda_rapida(request):
    if request.method == "POST":
        form = VendaRapidaForm(request.POST)
        if form.is_valid():
            venda = form.save(commit=False)
            # verificando se a quantidade solicitada é maior que a quantidade disponível
            quantidade = form.cleaned_data.get("quantidade")
            if quantidade > venda.ingresso.estoque_disponivel:
                messages.error(
                    request, "Quantidade informada acima do estoque disponível"
                )
                return redirect("venda_rapida")
            venda.titulo = venda.ingresso.titulo
            venda.local = venda.ingresso.local
            venda.data_horario_evento = venda.ingresso.data_horario
            venda.valor_pago = venda.ingresso.preco * venda.quantidade
            venda.save()
            # atualizando o estoque de ingressos se a venda tiver sido aprovada
            if venda.status == "A":
                venda.ingresso.estoque_disponivel -= venda.quantidade
                venda.ingresso.save()
            messages.success(request, "Venda registrada com sucesso!")
            return redirect("ingresso_list")
    else:
        form = VendaRapidaForm()
    context = {
        "form": form  # type: ignore
    }
    return render(request, "ingressos/venda_rapida_form.html", context)

@login_required
@user_passes_test(superuser_check)
def ingresso_registro_lote(request):
    # carregando os eventos do cache
    eventos = cache.get('eventos_carregados')

    # verificando se existem eventos cadastrados
    if not eventos:
        api = ApiMaracaService()
        eventos = api.obter_proximos_jogos()
        cache.set('eventos_carregados', eventos, 3_600*12)
        print('requisição realizada')

    # criando um novo campo para saber se o evento está cadastrado e convertendo str para datetime
    if eventos:
        # obtendo todas as datas cadastradas
        datas_cadastradas = set(Ingresso.objects.values_list('data_horario', flat=True))
        for evento in eventos:
            if isinstance(evento.get('dthr_evento'), str):
                evento['dthr_evento'] = timezone.make_aware(datetime.strptime(evento['dthr_evento'], '%Y-%m-%d %H:%M:%S'))
            evento['existe_cadastro'] = True if evento['dthr_evento'] in datas_cadastradas else False
    
    # carregando os eventos no contexto
    context = {
        'eventos': eventos
    }
    return render(request, 'ingressos/eventos_futuros.html', context)

@login_required
@user_passes_test(superuser_check)
def ingresso_create_via_api(request):
    pass
    
