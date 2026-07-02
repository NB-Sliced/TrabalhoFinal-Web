from django.db import models

class Reserva(models.Model):
    livro = models.ForeignKey('catalogo.Livro', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.livro.titulo} (x{self.quantidade})'