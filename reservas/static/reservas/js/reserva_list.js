const spanQuantidade = document.querySelector('.valor-qtd');
const botaoMais = document.querySelector('.btn-Mais');
const botaoMenos = document.querySelector('.btn-Menos');

botaoMais.addEventListener('click', function() {
    let quantidade = Number(spanQuantidade.textContent);
    quantidade = quantidade + 1;
    spanQuantidade.textContent = quantidade;
});

botaoMenos.addEventListener('click', function() {
    let quantidade = Number(spanQuantidade.textContent);

    if (quantidade - 1 <= 0) {
        const confirmar = confirm('Deseja remover este item da sua estante?');
        if (confirmar) {
            const linha = botaoMenos.closest('tr');
            linha.remove();
        }
    } else {
        quantidade = quantidade - 1;
        spanQuantidade.textContent = quantidade;
    }
});

const botaoRemover = document.querySelector('.btn-remover');

botaoRemover.addEventListener('click', function() {
    const confirmar = confirm('Remover este item da sua estante?');
    if (confirmar) {
        const linha = botaoRemover.closest('tr');
        linha.remove();
    }
});


