# Register your models here.
from django.contrib import admin
from .models import Leitor


@admin.register(Leitor)
class LeitorAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "cpf",
        "email",
        "telefone",
        "cidade",
        "curso_turma",
        "matricula",
        "login",
    )
    search_fields = ("nome", "cpf", "email", "matricula", "login")
    list_filter = ("cidade", "curso_turma")
    readonly_fields = ("criado_em",)