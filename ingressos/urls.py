from django.urls import path
from . import views

urlpatterns = [
    path(
        "comprar-ingresso/<int:id_ingresso>",
        views.comprar_ingresso,
        name="comprar_ingresso",
    ),
    path("cadastrar-ingresso/", views.cadastrar_ingresso, name="cadastrar_ingresso"),
    path("meus-ingressos/", views.exibir_meus_ingressos, name="meus_ingressos"),
    path(
        "json-detalhes-compra/<int:id_historico>",
        views.json_detalhes_compra,
        name="json_detalhes_compra",
    ),
    path(
        "todos-ingressos-comprados/",
        views.exibir_todos_ingressos_comprados,
        name="todos_ingressos_comprados",
    ),
    path(
        "editar-ingresso/<int:id_ingresso>/",
        views.editar_ingresso,
        name="editar_ingresso",
    ),
    path(
        "historico-venda/<int:id_historico>/",
        views.historico_venda_detail,
        name="historico_venda",
    ),
    path("lista-ingressos/", views.ingresso_list, name="ingresso_list"),
    path("deletar/<int:id_ingresso>/", views.ingresso_delete, name="ingresso_delete"),
    path("venda-rapida/", views.venda_rapida, name="venda_rapida"),
    path('eventos-futuros/', views.ingresso_registro_lote, name='ingresso_registro_lote'),
]
