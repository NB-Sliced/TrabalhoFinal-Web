from django.shortcuts import render

def cadastro(request):
    return render(request, 'usuarios/cadastro.html')