from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.cadastro, name='cadastro'),
]