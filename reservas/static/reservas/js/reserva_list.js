function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(function(cookie) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}

document.querySelectorAll('.btn-Mais, .btn-Menos').forEach(function(botao) {
    botao.addEventListener('click', function() {
        const acao = this.dataset.acao;
        const livroId = this.dataset.id;
        const linha = this.closest('tr');
        const spanQtd = linha.querySelector('.valor-qtd');

        if (acao === 'diminuir' && Number(spanQtd.textContent) <= 1) {
            const confirmar = confirm('Deseja remover este item da sua estante?');
            if (confirmar) {
                window.location.href = '/reserva/remover/' + livroId + '/';
            }
            return;
        }

        fetch('/reserva/atualizar/' + livroId + '/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: 'acao=' + acao,
        })
        .then(function(response) { return response.json(); })
        .then(function(data) {
            if (data.removido) {
                linha.remove();
            } else {
                spanQtd.textContent = data.quantidade;
            }
        });
    });
});