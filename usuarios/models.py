from django.db import models

# Create your models here.

class Leitor(models.Model):
    nome = models.CharField(max_length=120)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=180)
    cidade = models.CharField(max_length=80)
    curso_turma = models.CharField(max_length=100)
    matricula = models.CharField(max_length=30, unique=True)
    observacoes = models.TextField(blank=True)
    login = models.CharField(max_length=50, unique=True)
    senha = models.CharField(max_length=128)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Leitor"
        verbose_name_plural = "Leitores"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.login})"