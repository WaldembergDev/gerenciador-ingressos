from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClienteForm
from core.forms import CustomUserForm, CustomUserUpdateFormAdmin
from django.contrib import messages
from .models import Cliente
from django.contrib.auth.decorators import login_required, user_passes_test
from core.utils import superuser_check
from django.db.models import Sum


# Create your views here.
def criar_conta_cliente(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        cliente_form = ClienteForm(request.POST)
        custom_user_form = CustomUserForm(request.POST)
        if cliente_form.is_valid() and custom_user_form.is_valid():
            password = custom_user_form.cleaned_data.get("password")
            usuario = custom_user_form.save(commit=False)
            cliente = cliente_form.save(commit=False)
            usuario.set_password(password)
            cliente.usuario = usuario
            usuario.save()
            cliente.save()
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("criar_conta_cliente")
    else:
        cliente_form = ClienteForm()
        custom_user_form = CustomUserForm()
    context = {"cliente_form": cliente_form, "custom_user_form": custom_user_form}
    return render(request, "clientes/criar_conta_cliente.html", context=context)


@login_required
@user_passes_test(superuser_check)
def cliente_list(request):
    clientes = Cliente.objects.all()
    context = {"clientes": clientes}
    return render(request, "clientes/cliente_list.html", context)


@login_required
@user_passes_test(superuser_check)
def toggle_cliente_status(request, id_cliente):
    cliente = get_object_or_404(Cliente, id=id_cliente)
    if cliente.usuario.is_active:
        cliente.usuario.is_active = False
    else:
        cliente.usuario.is_active = True
    cliente.usuario.save()
    messages.success(request, "Cliente atualizado com sucesso!")
    return redirect("cliente_list")


@login_required
@user_passes_test(superuser_check)
def cliente_detail(request, id_cliente):
    cliente = get_object_or_404(Cliente, id=id_cliente)
    valor_total_compras = cliente.compras.filter(status="A").aggregate(
        total=Sum("valor_pago")
    )
    if request.method == "POST":
        cliente_form = ClienteForm(request.POST, instance=cliente)
        usuario_form = CustomUserUpdateFormAdmin(request.POST, instance=cliente.usuario)
        print(cliente_form.errors)
        if cliente_form.is_valid() and usuario_form.is_valid():
            usuario_form.save()
            cliente_form.save()
            messages.success(request, "Dados do cliente atualizado com sucesso!")
            return redirect("cliente_detail", cliente.id)
    else:
        cliente_form = ClienteForm(instance=cliente)
        usuario_form = CustomUserUpdateFormAdmin(instance=cliente.usuario)
    context = {
        "cliente_form": cliente_form,
        "usuario_form": usuario_form,
        "valor_total_compras": valor_total_compras,
    }
    return render(request, "clientes/cliente_detail.html", context)


@login_required
@user_passes_test(superuser_check)
def admin_create_client(request):
    if request.method == "POST":
        cliente_form = ClienteForm(request.POST)
        custom_user_form = CustomUserForm(request.POST)
        if cliente_form.is_valid() and custom_user_form.is_valid():
            password = custom_user_form.cleaned_data.get("password")
            usuario = custom_user_form.save(commit=False)
            cliente = cliente_form.save(commit=False)
            usuario.set_password(password)
            cliente.usuario = usuario
            usuario.save()
            cliente.save()
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("admin_create_client")
    else:
        cliente_form = ClienteForm()
        custom_user_form = CustomUserForm()
    context = {"cliente_form": cliente_form, "custom_user_form": custom_user_form}
    return render(request, "clientes/admin_create_client.html", context=context)
