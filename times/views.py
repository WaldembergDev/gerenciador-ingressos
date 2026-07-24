from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from times.models import Time
from .forms import TimeForm
from django.contrib import messages
from django.views.decorators.http import require_POST

# Create your views here.
@require_POST
def time_create(request: HttpRequest) -> HttpResponse:
    """ Cria novo registro no banco de dados.

    Args:
        request (HttpRequest): Objeto da requisição do Django

    Returns:
        HttpResponse: renderiza o formulário
    """
    
    form = TimeForm(request.POST, request.FILES)
    
    if form.is_valid():
        form.save()
        messages.success(request, 'Time criado com sucesso!')
        return redirect('time-list')
    else:
        print(form.errors)
        return redirect('time-list')


def time_list(request: HttpRequest) -> HttpResponse:
    """Lista os times registrados

    Args:
        request (HttpRequest): Objeto da requisição do Django

    Returns:
        HttpResponse: Renderiza o template com a lista de times
    """
    times = Time.objects.all()
    form = TimeForm()
    context = {
        'times': times,
        'form': form
    }
    return render(request, 'times/time_list.html', context)

