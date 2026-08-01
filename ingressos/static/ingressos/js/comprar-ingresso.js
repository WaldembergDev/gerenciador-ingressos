const modalConfirmacao = document.getElementById('modalConfirmacao');
const botaoConfirmar = document.getElementById('botaoConfirmar');
const inputQuantidade = document.getElementById('id_quantidade');
const spanQuantidade = document.getElementById('spanQuantidade');


modalConfirmacao.addEventListener('show.bs.modal', () => {
    if (spanQuantidade && inputQuantidade) {
        spanQuantidade.textContent = inputQuantidade.value;
    }
});


if (botaoConfirmar) {
    botaoConfirmar.addEventListener('click', () => {
        const formulario = document.querySelector('#formularioComprarIngresso');
        if (formulario) {
            formulario.submit();
        }
    });
}