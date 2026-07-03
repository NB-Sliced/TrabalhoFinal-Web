from django.shortcuts import render, redirect, get_object_or_404
from catalogo.models import Livro


def ver_reserva(request):
    return render(request, 'reservas/reserva_list.html')


def adicionar_ao_carrinho(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)

    carrinho = request.session.get('carrinho', {})
    livro_id_str = str(livro_id)
    carrinho[livro_id_str] = carrinho.get(livro_id_str, 0) + 1
    request.session['carrinho'] = carrinho

    return redirect('reservas:ver_reserva')