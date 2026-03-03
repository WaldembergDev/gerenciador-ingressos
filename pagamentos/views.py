from django.shortcuts import render
from .utils import Asaas
from django.http import HttpResponse

# Create your views here.
def criar_pagamento(request):
    return HttpResponse('Teste')