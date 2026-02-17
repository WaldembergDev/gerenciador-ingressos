from django.http import HttpResponse
from django.shortcuts import render, redirect
from ingressos.models import Ingresso
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import EmailAuthenticationForm, AcessoGeralForm
from .models import AcessoGeral
from django.db.models import Q
from django.utils import timezone

from django.contrib.auth.hashers import check_password

# Create your views here.
def acesso_inicial(request):
    if request.session.get('acesso_geral'):
        return redirect('home')
    if request.method == 'POST':
        form_acesso = AcessoGeralForm(request.POST)
        if form_acesso.is_valid():
            senha = form_acesso.cleaned_data.get('senha')
            senha_acesso = AcessoGeral.objects.order_by('-id').first().senha
            senha_valida = check_password(senha, senha_acesso)
            if senha_valida:
                request.session['acesso_geral'] = senha_acesso
                return redirect('home')
            else:
                messages.error(request, 'Senha não confere!')     
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