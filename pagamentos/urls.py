from django.urls import path
from . import views


urlpatterns = [
    path(
        "novo-pagamento/<uuid:id_historico_compra>/",
        views.criar_checkout,
        name="criar_pagamento",
    ),
    path("webook/", views.receber_webhook, name="receber_webhook"),
]
