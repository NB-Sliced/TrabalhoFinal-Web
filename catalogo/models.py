from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255, blank=True)
    imagem = models.URLField(blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    editora = models.CharField(max_length=100)
    ano = models.IntegerField()
    paginas = models.IntegerField()
    sinopse = models.TextField()
    imagem_capa = models.URLField(blank=True)
    disponivel = models.BooleanField(default=True)
    emprestimos = models.IntegerField(default=0)
    genero = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='livros')

    def __str__(self):
        return self.titulo