from re import S

from django.shortcuts import get_object_or_404, render, redirect
from ingressos.models import Ingresso
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import (
    EmailAuthenticationForm,
    AcessoGeralForm,
    CustomUserUpdateForm,
    ResetSenhaForm,
    AcessoGeralFormCreate
)
from .models import AcessoGeral
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from .utils import superuser_check
from clientes.models import Cliente
from clientes.forms import ClienteForm


User = get_user_model()


# Create your views here.
def acesso_inicial(request):
    if request.session.get("acesso_geral"):
        return redirect("home")
    if request.method == "POST":
        form_acesso = AcessoGeralForm(request.POST)
        if form_acesso.is_valid():
            senha = form_acesso.cleaned_data.get("senha")
            obj_acesso_geral = AcessoGeral.objects.order_by("-id").first()
            if not obj_acesso_geral:
                messages.error(request, "Contate o administrador do sistema!")
                return redirect("acesso_inicial")
            senha_acesso = obj_acesso_geral.senha
            senha_valida = check_password(senha, senha_acesso)
            if senha_valida:
                request.session["acesso_geral"] = senha_acesso
                return redirect("home")
            else:
                messages.error(request, "Senha não confere!")
                return redirect("acesso_inicial")
    else:
        form_acesso = AcessoGeralForm()
    context = {"form_acesso": form_acesso}
    return render(request, "core/acesso_inicial.html", context=context)


def home(request):
    query = request.GET.get("q")
    agora = timezone.now()
    ingressos = Ingresso.objects.filter(
        data_horario__gte=agora, status=Ingresso.StatusIngresso.ATIVO
    ).order_by("data_horario")

    if request.GET.get("q"):
        ingressos = ingressos.filter(
            (Q(titulo__icontains=query) | Q(descricao__icontains=query))
            & Q(data_horario__gte=agora)
        ).distinct()

    context = {"ingressos": ingressos, "query": query}
    return render(request, "core/home.html", context)


def login(request):
    next = None
    # verificando se o usuário está logado
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            proxima_pagina = request.POST.get("next")
            print(proxima_pagina)
            user = form.get_user()
            auth_login(request, user)
            # verificando se existe página a ser redirecionada
            if proxima_pagina:
                return redirect(proxima_pagina)
            return redirect("home")
    else:
        form = EmailAuthenticationForm()
        next = request.GET.get("next")
    context = {"form": form, "next": next}
    return render(request, "core/login.html", context=context)


@login_required
@user_passes_test(superuser_check)
def admin_resetar_senha_usuario(request, id_usuario):
    usuario = get_object_or_404(User, id=id_usuario)
    usuario.set_password("12345678")
    usuario.save()
    messages.success(request, "Senha alterada com sucesso!")
    return redirect("cliente_list")


@login_required
def minha_conta(request):
    perfil_usuario = request.user
    perfil_cliente = Cliente.objects.filter(usuario=perfil_usuario).first()
    if request.method == "POST":
        form_custom_user = CustomUserUpdateForm(request.POST, instance=perfil_usuario)
        form_cliente = ClienteForm(request.POST, instance=perfil_cliente)
        if form_custom_user.is_valid() and form_cliente.is_valid():
            form_custom_user.save()
            form_cliente.save()
            messages.success(request, "Dados atualizados com sucesso!")
            return redirect("minha_conta")
    else:
        form_custom_user = CustomUserUpdateForm(instance=perfil_usuario)
        form_cliente = ClienteForm(instance=perfil_cliente)
        form_reset_password = ResetSenhaForm()

    context = {
        "form_custom_user": form_custom_user,
        "form_cliente": form_cliente,
        "form_reset_password": form_reset_password,
    }
    return render(request, "core/minha_conta.html", context)


@login_required
def reset_senha(request):
    usuario = request.user
    form = ResetSenhaForm(request.POST, instance=usuario)
    if form.is_valid():
        password = form.cleaned_data["password"]
        confirmacao_password = form.cleaned_data["confirmacao_password"]
        if password != confirmacao_password:
            messages.error(request, "As senhas digitadas não são iguais!")
            return redirect("minha_conta")
        usuario.set_password(password)
        usuario.save()
        messages.success(request, "Senha atualizada com sucesso!")
        return redirect("minha_conta")
    else:
        messages.error(request, "Erro ao validar o formulário")
        return redirect("minha_conta")


@login_required
@user_passes_test(superuser_check) # type:ignore
def acesso_geral_create(request):
    if request.method == "POST":
        form = AcessoGeralFormCreate(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('senha')
            confirmacao_password = form.cleaned_data.get('confirmacao_password')
            if password != confirmacao_password:
                messages.error(request, 'As senhas digitadas não são iguais!')      
                return redirect('acesso_geral_create')
            form.save()
            messages.success(request, 'Senha atualizada com sucesso!')
            return redirect('home')
    else:
        form = AcessoGeralFormCreate()
    context = {"form": form} # type: ignore
    return render(request, "core/acesso_geral_form.html", context)
