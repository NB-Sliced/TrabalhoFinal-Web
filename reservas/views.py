from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from catalogo.models import Livro


def ver_reserva(request):
    carrinho = request.session.get("carrinho", {})
    itens = list(carrinho.values())
    total = sum(item["quantidade"] for item in itens)
    return render(request, "reservas/reserva_list.html", {
        "itens": itens,
        "total": total,
    })


def adicionar_ao_carrinho(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    carrinho = request.session.get("carrinho", {})
    chave = str(livro_id)

    if chave in carrinho:
        carrinho[chave]["quantidade"] += 1
    else:
        carrinho[chave] = {
            "livro_id": livro_id,
            "titulo": livro.titulo,
            "autor": livro.autor,
            "imagem": livro.imagem_capa,
            "quantidade": 1,
        }

    request.session["carrinho"] = carrinho
    request.session.modified = True
    messages.success(request, f'"{livro.titulo}" adicionado à sua estante.')
    return redirect(request.META.get("HTTP_REFERER", "/"))


@require_POST
def atualizar_quantidade(request, livro_id):
    acao = request.POST.get("acao")  # "aumentar" ou "diminuir"
    carrinho = request.session.get("carrinho", {})
    chave = str(livro_id)

    if chave not in carrinho:
        return JsonResponse({"erro": "Item não encontrado."}, status=404)

    if acao == "aumentar":
        carrinho[chave]["quantidade"] += 1
    elif acao == "diminuir":
        carrinho[chave]["quantidade"] -= 1
        if carrinho[chave]["quantidade"] <= 0:
            del carrinho[chave]
            request.session["carrinho"] = carrinho
            request.session.modified = True
            return JsonResponse({"removido": True})

    request.session["carrinho"] = carrinho
    request.session.modified = True
    return JsonResponse({"quantidade": carrinho[chave]["quantidade"]})


def remover_item(request, livro_id):
    carrinho = request.session.get("carrinho", {})
    chave = str(livro_id)
    carrinho.pop(chave, None)
    request.session["carrinho"] = carrinho
    request.session.modified = True
    return redirect("reservas:ver_reserva")


def finalizar_reserva(request):
    request.session["carrinho"] = {}
    request.session.modified = True
    messages.success(request, "Reserva finalizada com sucesso!")
    return redirect("reservas:ver_reserva")
