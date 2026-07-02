from django.urls import path

from . import views

app_name = "catalogo"

urlpatterns = [
    path('', views.index, name='home'),
    path('categoria/<slug:slug>/', views.categoria_detalhe, name='categoria_detalhe'),
    path('livros/<int:livro_id>/', views.detalhes_livro, name='detalhes_livro'),
    path('api/categorias/', views.api_categorias, name='api_categorias'),
    path('api/livros/', views.api_livros, name='api_livros'),
]