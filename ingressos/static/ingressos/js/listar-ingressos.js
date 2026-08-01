const btnConfirmacao = document.querySelector('.bntConfirmarExclusao');
const btnModalConfirmacao = document.querySelector('.btnModalConfirmacao');
const modalConfirmacaoExclusao = document.getElementById('modalConfirmacaoExclusao');
const formExclusao = document.getElementById("formExclusao");
let idIngresso = null;

modalConfirmacaoExclusao.addEventListener('show.bs.modal', event => {
    const botao = event.relatedTarget;
    idIngresso = botao.getAttribute('data-ingresso-id');
})

btnModalConfirmacao.addEventListener('click', () => {
    console.log('entrei')
    if (idIngresso) {
        formExclusao.action = `/ingressos/deletar/${idIngresso}/`;
        formExclusao.submit();
    }
})