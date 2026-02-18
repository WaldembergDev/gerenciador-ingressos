from django.urls import path
from . import views

urlpatterns = [
    path('comprar-ingresso/<uuid:id_ingresso>', views.comprar_ingresso, name='comprar_ingresso'),
    path('visualizar-ingresso/<uuid:id_ingresso>', views.visualizar_ingresso, name='visualizar_ingresso'),
    path('cadastrar-ingresso/', views.cadastrar_ingresso, name='cadastrar_ingresso'),
    path('meus-ingressos/', views.exibir_meus_ingressos, name='meus_ingressos'),
    path('json-detalhes-compra/<uuid:id_historico>', views.json_detalhes_compra, name='json_detalhes_compra'),
    path('todos-ingressos-comprados/', views.exibir_todos_ingressos_comprados, name='todos_ingressos_comprados'),
    path('editar-ingresso/<uuid:id_ingresso>', views.editar_ingresso, name='editar_ingresso'),
    path('historico-venda/<uuid:id_historico>/', views.historico_venda_detail, name='historico_venda')
]
