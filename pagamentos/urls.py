
from django.urls import path
from . import views


urlpatterns = [
    path('novo-pagamento/<uuid:id_historico_compra>/', views.criar_pagamento, name='criar_pagamento'),
]