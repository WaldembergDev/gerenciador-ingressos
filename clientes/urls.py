from django.urls import path
from . import views

urlpatterns = [
    path('criar-conta/', views.criar_conta_cliente, name='criar_conta_cliente'),
    path('lista-clientes/', views.cliente_list, name='cliente_list'),
    path('toggle-cliente-status/<uuid:id_cliente>/', views.toggle_cliente_status, name="toggle_cliente_status"),
    path('cliente-detalhes/<uuid:id_cliente>/', views.cliente_detail, name='cliente_detail')
]
