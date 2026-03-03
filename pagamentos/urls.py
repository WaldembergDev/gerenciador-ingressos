
from django.urls import path
from . import views


urlpatterns = [
    path('', views.criar_pagamento, name='criar_pagamento'),
]