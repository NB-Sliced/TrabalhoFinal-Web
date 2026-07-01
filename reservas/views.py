from django.shortcuts import render

def ver_reserva(request):
    return render(request, 'reservas/reserva_list.html')