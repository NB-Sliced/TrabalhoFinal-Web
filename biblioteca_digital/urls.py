from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalogo.urls")),
    path("usuarios/", include("usuarios.urls")),
    path("reserva/", include("reservas.urls")),
]