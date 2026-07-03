import json

from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Leitor


CAMPOS_OBRIGATORIOS = [
    "nome",
    "cpf",
    "email",
    "telefone",
    "endereco",
    "cidade",
    "curso_turma",
    "matricula",
    "login",
    "senha",
    "confirmar_senha",
]


def cadastro_leitor(request):
    """
    Página 4 do trabalho:
    mostra o formulário de cadastro do leitor usando método GET.
    """
    return render(request, "usuarios/cadastro.html")


def confirmar_cadastro_leitor(request):
    """
    Endpoint GET:
    recebe os dados do formulário, valida, salva no banco e mostra confirmação.
    """
    dados = request.GET

    erros = []

    for campo in CAMPOS_OBRIGATORIOS:
        if not dados.get(campo):
            erros.append(f"O campo {campo.replace('_', ' ')} é obrigatório.")

    if dados.get("senha") != dados.get("confirmar_senha"):
        erros.append("A confirmação da senha precisa ser igual à senha.")

    if dados.get("email") and Leitor.objects.filter(email=dados.get("email")).exists():
        erros.append("Já existe um leitor cadastrado com este e-mail.")

    if dados.get("cpf") and Leitor.objects.filter(cpf=dados.get("cpf")).exists():
        erros.append("Já existe um leitor cadastrado com este CPF.")

    if dados.get("matricula") and Leitor.objects.filter(matricula=dados.get("matricula")).exists():
        erros.append("Já existe um leitor cadastrado com esta matrícula.")

    if dados.get("login") and Leitor.objects.filter(login=dados.get("login")).exists():
        erros.append("Já existe um leitor cadastrado com este login.")

    if erros:
        return render(
            request,
            "usuarios/cadastro.html",
            {
                "erros_servidor": erros,
                "dados": dados,
            },
        )

    leitor = Leitor.objects.create(
        nome=dados.get("nome"),
        cpf=dados.get("cpf"),
        email=dados.get("email"),
        telefone=dados.get("telefone"),
        endereco=dados.get("endereco"),
        cidade=dados.get("cidade"),
        curso_turma=dados.get("curso_turma"),
        matricula=dados.get("matricula"),
        observacoes=dados.get("observacoes", ""),
        login=dados.get("login"),
        senha=make_password(dados.get("senha")),
    )

    return render(request, "usuarios/cadastro_confirmado.html", {"leitor": leitor})


def login_leitor(request):
    """
    Formulário de login.
    Necessário para cobrir o critério backend de autenticação.
    """
    return render(request, "usuarios/login.html")


@require_POST
def autenticar_leitor(request):
    """
    Endpoint POST:
    autentica login/e-mail + senha.
    Se estiver correto, envia para a tela de reserva.
    """
    identificador = request.POST.get("identificador", "").strip()
    senha = request.POST.get("senha", "")

    leitor = (
        Leitor.objects.filter(login=identificador).first()
        or Leitor.objects.filter(email=identificador).first()
    )

    if leitor and check_password(senha, leitor.senha):
        request.session["leitor_id"] = leitor.id
        request.session["leitor_nome"] = leitor.nome
        messages.success(request, f"Bem-vindo(a), {leitor.nome}!")

        return redirect("/reservas/")

    messages.error(request, "Login/e-mail ou senha inválidos.")
    return redirect(reverse("usuarios:login"))


@csrf_exempt
@require_POST
def api_cadastro_leitor(request):
    """
    Endpoint POST extra para cadastro.
    Ele existe para atender o critério backend que pede endpoint POST de cadastro.
    """
    try:
        payload = json.loads(request.body.decode("utf-8")) if request.body else request.POST
    except json.JSONDecodeError:
        return JsonResponse({"erro": "JSON inválido."}, status=400)

    obrigatorios = [
        "nome",
        "cpf",
        "email",
        "telefone",
        "endereco",
        "cidade",
        "curso_turma",
        "matricula",
        "login",
        "senha",
    ]

    faltando = [campo for campo in obrigatorios if not payload.get(campo)]

    if faltando:
        return JsonResponse(
            {
                "erro": "Campos obrigatórios ausentes.",
                "campos": faltando,
            },
            status=400,
        )

    if payload.get("senha") != payload.get("confirmar_senha", payload.get("senha")):
        return JsonResponse({"erro": "A confirmação da senha não confere."}, status=400)

    if Leitor.objects.filter(email=payload.get("email")).exists():
        return JsonResponse({"erro": "Já existe leitor com este e-mail."}, status=400)

    if Leitor.objects.filter(cpf=payload.get("cpf")).exists():
        return JsonResponse({"erro": "Já existe leitor com este CPF."}, status=400)

    if Leitor.objects.filter(matricula=payload.get("matricula")).exists():
        return JsonResponse({"erro": "Já existe leitor com esta matrícula."}, status=400)

    if Leitor.objects.filter(login=payload.get("login")).exists():
        return JsonResponse({"erro": "Já existe leitor com este login."}, status=400)

    leitor = Leitor.objects.create(
        nome=payload.get("nome"),
        cpf=payload.get("cpf"),
        email=payload.get("email"),
        telefone=payload.get("telefone"),
        endereco=payload.get("endereco"),
        cidade=payload.get("cidade"),
        curso_turma=payload.get("curso_turma"),
        matricula=payload.get("matricula"),
        observacoes=payload.get("observacoes", ""),
        login=payload.get("login"),
        senha=make_password(payload.get("senha")),
    )

    return JsonResponse(
        {
            "mensagem": "Leitor cadastrado com sucesso.",
            "id": leitor.id,
            "nome": leitor.nome,
        },
        status=201,
    )


@csrf_exempt
@require_POST
def api_login_leitor(request):
    """
    Endpoint POST extra para autenticação.
    """
    try:
        payload = json.loads(request.body.decode("utf-8")) if request.body else request.POST
    except json.JSONDecodeError:
        return JsonResponse({"erro": "JSON inválido."}, status=400)

    identificador = payload.get("identificador") or payload.get("login") or payload.get("email")
    senha = payload.get("senha", "")

    leitor = (
        Leitor.objects.filter(login=identificador).first()
        or Leitor.objects.filter(email=identificador).first()
    )

    if leitor and check_password(senha, leitor.senha):
        return JsonResponse(
            {
                "autenticado": True,
                "leitor_id": leitor.id,
                "nome": leitor.nome,
            }
        )

    return JsonResponse(
        {
            "autenticado": False,
            "erro": "Credenciais inválidas.",
        },
        status=401,
    )

def logout_leitor(request):
    request.session.flush()
    messages.success(request, "Você saiu da sua conta.")
    return redirect(reverse("catalogo:home"))