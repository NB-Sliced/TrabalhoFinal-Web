from django.shortcuts import render

def home(request):
    return render(request,'catalogo/home.html')