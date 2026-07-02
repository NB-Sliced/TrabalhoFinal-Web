from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Categoria, Livro

def home(request):
    return render(request,'catalogo/home.html')

def index(request):
    categorias = Categoria.objects.all()
    mais_emprestados = Livro.objects.order_by('-emprestimos')[:5]
    return render(request, 'catalogo/index.html', {
        'categorias': categorias,
        'mais_emprestados': mais_emprestados,
    })

def categoria_detalhe(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    livros = Livro.objects.filter(genero=categoria)
    return render(request, 'catalogo/categoria.html', {
        'categoria': categoria,
        'livros': livros,
    })

def api_categorias(request):
    categorias = list(Categoria.objects.values('id', 'nome', 'descricao', 'imagem', 'slug'))
    return JsonResponse(categorias, safe=False)

def api_livros(request):
    categoria_id = request.GET.get('categoria_id')
    livros = Livro.objects.filter(genero_id=categoria_id).values(
        'id', 'titulo', 'autor', 'editora', 'ano', 'imagem_capa', 'disponivel', 'emprestimos'
    )
    return JsonResponse(list(livros), safe=False)


