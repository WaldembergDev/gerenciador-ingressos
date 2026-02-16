from .models import AcessoGeral
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect

def middleware_acesso_inicial(get_response):
    def middleware(request):
        if (not request.session.get('acesso_geral') and
            not request.path == '/core/acesso-inicial/' and
            not request.path.startswith('/admin/')):
            return redirect('acesso_inicial')
        
        response = get_response(request)        

        return response   

    return middleware