from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('', views.ver_reserva, name='ver_reserva'),
    path('adicionar/<int:livro_id>/', views.adicionar_ao_carrinho, name='adicionar'),
]