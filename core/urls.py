from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login, name='core_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('acesso-inicial/', views.acesso_inicial, name='acesso_inicial'),
    path('admin-resetar-senha-cliente/<uuid:id_usuario>/', views.admin_resetar_senha_cliente, name='admin_resetar_senha_cliente')
]