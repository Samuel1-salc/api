from django.http import HttpResponse
from django.shortcuts import render

def test_view(request):
    return HttpResponse("Teste de view funcionando!")

def home_view(request):
    return HttpResponse("Bem-vindo à página inicial!")
