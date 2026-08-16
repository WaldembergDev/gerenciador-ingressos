from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from times.models import Time
from .forms import TimeForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from core.utils import superuser_check


# Create your views here.
@require_POST
@user_passes_test(superuser_check)
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

@user_passes_test(superuser_check)
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

@user_passes_test(superuser_check)
def time_edit(request: HttpRequest, id_time: int) -> HttpResponse:
    """ Edita um time com base no id """
    time = get_object_or_404(Time, id=id_time)
    if request.method == 'POST':
        form = TimeForm(request.POST, request.FILES, instance=time)
        if form.is_valid():
            form.save()
            messages.success(request, 'Time atualizado com sucesso!')
            return redirect('time-list')
    else:
        form = TimeForm(instance=time)
    context = {
        'form': form
    }
    return render(request, 'times/partials/_modal_editar.html', context)