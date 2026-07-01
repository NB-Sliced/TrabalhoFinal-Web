from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reserva/', include('reservas.urls')),
    path('', include('catalogo.urls')),
    path('cadastro', include('usuarios.urls'))
]
