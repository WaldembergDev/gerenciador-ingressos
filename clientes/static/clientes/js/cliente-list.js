const modalConfirmarAlteracao = document.getElementById('modalConfirmarAlteracao');
let formAlteracao = document.getElementById('formAlteracao');
let btnConfirmacao = document.querySelector('.btnConfirmacao');
let corpoModalAcao = document.getElementById('corpoModalAcao');
let corpoModalCliente = document.getElementById('corpoModalCliente');
let idCliente = null;
let statusCliente = null;
let cliente = null;

modalConfirmarAlteracao.addEventListener('show.bs.modal', (event) => {
    const botao = event.relatedTarget;
    idCliente = botao.getAttribute('data-cliente-id');
    cliente = botao.getAttribute('data-cliente-nome');
    statusCliente = botao.getAttribute('data-cliente-status');

    corpoModalCliente.textContent = cliente;

    if (statusCliente === 'Inativo') {
        corpoModalAcao.textContent = 'ativação';

    } else {
        corpoModalAcao.textContent = 'inativação';
    }
});

btnConfirmacao.addEventListener('click', () => {
    console.log('Entrei aqui')
    if (idCliente) {
        formAlteracao.action = `/clientes/toggle-cliente-status/${idCliente}/`;
        formAlteracao.submit();
    }
})