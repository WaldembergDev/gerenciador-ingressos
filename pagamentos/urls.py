from django.urls import path
from . import views


urlpatterns = [
    path(
        "novo-pagamento/<int:id_historico_compra>/",
        views.criar_checkout,
        name="criar_pagamento",
    ),
    path("webhook/", views.receber_webhook, name="receber_webhook"),
    path(
        "sucesso/<int:id_historico_compra>/",
        views.confirmacao_pagamento,
        name="confirmacao_pagamento",
    ),
    path("cancelado/", views.cancelamento_pedido, name="cancelamento_pedido"),
]
