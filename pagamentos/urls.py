
from django.urls import path
from . import views


urlpatterns = [
    path('ingressos/', views.criar_pagamento, name='criar_pagamento'),
]