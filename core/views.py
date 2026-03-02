from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from ingressos.models import Ingresso
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import EmailAuthenticationForm, AcessoGeralForm
from .models import AcessoGeral, CustomUser
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from .utils import superuser_check


User = get_user_model()

# Create your views here.
def acesso_inicial(request):
    if request.session.get('acesso_geral'):
        return redirect('home')
    if request.method == 'POST':
        form_acesso = AcessoGeralForm(request.POST)
        if form_acesso.is_valid():
            senha = form_acesso.cleaned_data.get('senha')
            obj_acesso_geral = AcessoGeral.objects.order_by('-id').first()
            if not obj_acesso_geral:
                messages.error(request, 'Contate o administrador do sistema!')
                return redirect('acesso_inicial')
            senha_acesso = obj_acesso_geral.senha
            senha_valida = check_password(senha, senha_acesso)
            if senha_valida:
                request.session['acesso_geral'] = senha_acesso
                return redirect('home')
            else:
                messages.error(request, 'Senha não confere!')
                return redirect('acesso_inicial')    
    else:
        form_acesso = AcessoGeralForm()
    context = {
        'form_acesso': form_acesso
    }
    return render(request, 'core/acesso_inicial.html', context=context)


def home(request):
    query = request.GET.get('q')
    agora = timezone.now()
    if request.GET.get('q'):
        ingressos = Ingresso.objects.filter(
            (Q(titulo__icontains=query) | Q(descricao__icontains=query)) &
             Q(data_horario__gte=agora)
        ).distinct()
    else:
        
        ingressos = Ingresso.objects.filter(
            data_horario__gte=agora
            ).order_by('data_horario')
    context = {
        'ingressos': ingressos,
        'query': query
    }
    return render(request, 'core/home.html', context)

def login(request):
    next = None
    # verificando se o usuário está logado
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            proxima_pagina = request.POST.get('next')
            print(proxima_pagina)
            user = form.get_user()
            auth_login(request, user)
            # verificando se existe página a ser redirecionada
            if proxima_pagina:
                return redirect(proxima_pagina)
            return redirect('home')
    else:
        form = EmailAuthenticationForm()
        next = request.GET.get('next')
    context = {
        'form': form,
        'next': next
    }
    return render(request, 'core/login.html', context=context)


@login_required
@user_passes_test(superuser_check)
def admin_resetar_senha_usuario(request, id_usuario):
    usuario = get_object_or_404(User, id=id_usuario)
    usuario.set_password('12345678')
    usuario.save()
    messages.success(request, 'Senha alterada com sucesso!')
    return redirect('cliente_list')