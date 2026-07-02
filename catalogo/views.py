from django.apps import apps
from django.shortcuts import get_object_or_404, render


LIVRO_EXEMPLO = {
    "id": 1,
    "titulo": "Clean Code",
    "autor": "Robert C. Martin",
    "editora": "Prentice Hall",
    "ano": 2008,
    "sinopse": "Um guia sobre boas práticas para escrever código simples, legível e fácil de manter.",
    "numero_paginas": 464,
    "genero": "Tecnologia",
    "disponibilidade": "Disponível",
    "imagem_capa": "/static/img/51E2055ZGUL._SL1000_.jpg",
    "topicos": [
        "Boas práticas de programação",
        "Nomes significativos",
        "Funções pequenas e objetivas",
        "Tratamento de erros",
    ],
}


def _valor(objeto, campo, padrao=""):
    if isinstance(objeto, dict):
        return objeto.get(campo, padrao)

    return getattr(objeto, campo, padrao)


def _imagem_url(livro):
    imagem = _valor(livro, "imagem_capa") or _valor(livro, "imagem")

    if hasattr(imagem, "url"):
        return imagem.url

    return imagem or "/static/img/51E2055ZGUL._SL1000_.jpg"


def _genero(livro):
    genero = _valor(livro, "genero")

    if genero:
        return genero

    categoria = _valor(livro, "categoria")

    return getattr(categoria, "nome", categoria) or "Categoria não informada"


def _disponibilidade(livro):
    disponibilidade = _valor(livro, "disponibilidade")

    if isinstance(disponibilidade, bool):
        return "Disponível" if disponibilidade else "Indisponível"

    return disponibilidade or "Disponibilidade não informada"


def home_placeholder(request):
    """
    Tela temporária para o link Início não quebrar.
    O Membro 1 depois pode substituir isso pela home real.
    """
    return render(request, "catalogo/home_placeholder.html")


def detalhes_livro(request, livro_id):
    """
    Página 3:
    detalhes do livro.

    Essa view tenta usar o Model Livro do Membro 1.
    Se o Model Livro ainda não existir, ela mostra um livro de exemplo.
    """
    try:
        Livro = apps.get_model("catalogo", "Livro")
        livro = get_object_or_404(Livro, id=livro_id)
        usando_exemplo = False

    except LookupError:
        livro = LIVRO_EXEMPLO
        usando_exemplo = True

    contexto_livro = {
        "id": _valor(livro, "id", livro_id),
        "titulo": _valor(livro, "titulo", "Título não informado"),
        "autor": _valor(livro, "autor", "Autor não informado"),
        "editora": _valor(livro, "editora", "Editora não informada"),
        "ano": _valor(livro, "ano", "Ano não informado"),
        "sinopse": _valor(livro, "sinopse", "Sinopse não informada."),
        "numero_paginas": _valor(
            livro,
            "numero_paginas",
            _valor(livro, "paginas", "Não informado"),
        ),
        "genero": _genero(livro),
        "disponibilidade": _disponibilidade(livro),
        "imagem_capa": _imagem_url(livro),
        "topicos": _valor(livro, "topicos", LIVRO_EXEMPLO["topicos"]),
    }

    return render(
        request,
        "catalogo/detalhes_livro.html",
        {
            "livro": contexto_livro,
            "usando_exemplo": usando_exemplo,
        },
    )