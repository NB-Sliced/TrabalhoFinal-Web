from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("cadastro/", views.cadastro_leitor, name="cadastro"),
    path("cadastro/confirmar/", views.confirmar_cadastro_leitor, name="cadastro_confirmar"),

    path("login/", views.login_leitor, name="login"),
    path("login/autenticar/", views.autenticar_leitor, name="autenticar"),

    path("api/cadastro/", views.api_cadastro_leitor, name="api_cadastro"),
    path("api/login/", views.api_login_leitor, name="api_login"),
    path("logout/", views.logout_leitor, name="logout"),
]