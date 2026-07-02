document.addEventListener('DOMContentLoaded', function () {
    const cadastroForm = document.querySelector('#cadastroLeitorForm');
    const loginForm = document.querySelector('#loginLeitorForm');

    function valor(id) {
        const campo = document.querySelector('#' + id);
        return campo ? campo.value.trim() : '';
    }

    function mostrarErro(id, mensagem) {
        const campo = document.querySelector('#' + id);
        const erro = document.querySelector('[data-erro="' + id + '"]');

        if (campo) {
            campo.closest('.campo').classList.toggle('invalido', Boolean(mensagem));
        }

        if (erro) {
            erro.textContent = mensagem || '';
        }
    }

    function limparErros(ids) {
        ids.forEach(function (id) {
            mostrarErro(id, '');
        });
    }

    function validarObrigatorio(id, nomeCampo) {
        if (!valor(id)) {
            mostrarErro(id, nomeCampo + ' é obrigatório.');
            return false;
        }

        mostrarErro(id, '');
        return true;
    }

    function validarCadastro() {
        const campos = [
            ['nome', 'Nome completo'],
            ['cpf', 'CPF'],
            ['email', 'E-mail'],
            ['telefone', 'Telefone'],
            ['endereco', 'Endereço'],
            ['cidade', 'Cidade'],
            ['curso_turma', 'Curso/Turma'],
            ['matricula', 'Matrícula institucional'],
            ['login', 'Login'],
            ['senha', 'Senha'],
            ['confirmar_senha', 'Confirmação da senha']
        ];

        limparErros(campos.map(function (item) {
            return item[0];
        }));

        let valido = true;

        campos.forEach(function (item) {
            if (!validarObrigatorio(item[0], item[1])) {
                valido = false;
            }
        });

        const cpf = valor('cpf');
        const email = valor('email');
        const telefone = valor('telefone');
        const senha = valor('senha');
        const confirmarSenha = valor('confirmar_senha');

        if (cpf && !/^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$/.test(cpf)) {
            mostrarErro('cpf', 'Digite um CPF no formato 000.000.000-00.');
            valido = false;
        }

        if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            mostrarErro('email', 'Digite um e-mail válido.');
            valido = false;
        }

        if (telefone && !/^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$/.test(telefone)) {
            mostrarErro('telefone', 'Digite um telefone válido. Ex.: (11) 99999-9999.');
            valido = false;
        }

        if (senha && senha.length < 6) {
            mostrarErro('senha', 'A senha deve ter pelo menos 6 caracteres.');
            valido = false;
        }

        if (senha && confirmarSenha && senha !== confirmarSenha) {
            mostrarErro('confirmar_senha', 'As senhas precisam ser iguais.');
            valido = false;
        }

        return valido;
    }

    if (cadastroForm) {
        cadastroForm.addEventListener('submit', function (event) {
            if (!validarCadastro()) {
                event.preventDefault();
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            let valido = true;

            if (!validarObrigatorio('identificador', 'Login ou e-mail')) {
                valido = false;
            }

            if (!validarObrigatorio('senha_login', 'Senha')) {
                valido = false;
            }

            if (!valido) {
                event.preventDefault();
            }
        });
    }
});