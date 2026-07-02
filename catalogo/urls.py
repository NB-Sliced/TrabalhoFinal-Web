from django.urls import path

from . import views

app_name = "catalogo"

urlpatterns = [
    path("", views.home_placeholder, name="home"),
    path("livros/<int:livro_id>/", views.detalhes_livro, name="detalhes_livro"),
]