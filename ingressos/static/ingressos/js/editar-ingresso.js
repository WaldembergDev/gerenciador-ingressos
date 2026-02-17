/* Função que cancela as alterações */
function cancelarAlteracoes(){
    let btnCancelarAlteracoes = document.querySelector('.btnCancelarAlteracoes');
    btnCancelarAlteracoes.addEventListener('click', function(event){
        window.location.href = btnCancelarAlteracoes.dataset.href;
});
}


/* Função que confirma as alterações */
function confirmarAlteracoes(){
    const formularioConfirmacao = document.getElementById('formularioConfirmacao');
    formularioConfirmacao.addEventListener('submit', function(event){
        event.preventDefault();
        const formularioDados = document.getElementById('formularioDados');
        formularioDados.submit();       
});
}
// Aguardando a página estar pronta
document.addEventListener('DOMContentLoaded', function(){
    /* Chamando as funções */
    cancelarAlteracoes();
    confirmarAlteracoes();
});