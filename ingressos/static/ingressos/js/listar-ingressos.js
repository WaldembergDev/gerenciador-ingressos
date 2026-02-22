function confirmarExlusão(){
    const botoes = document.querySelectorAll('.bntConfirmarExclusao');
    // Percorrendo todos os botões
    botoes.forEach(botao => {
        // ouvindo se o botão é clicado
        botao.addEventListener('click', function(e){
            // Obtendo dados do botão
            const idIngresso = botao.getAttribute('data-ingresso-id');
            const evento = botao.getAttribute('data-ingresso-evento');
            // selecionando o modal do bootstrap
            const modalBootstrap = document.getElementById('modalConfirmacaoExclusao');
            // instanciando um modal bootstrap
            const modal = new bootstrap.Modal(modalBootstrap);
            // exibindo o modal
            modal.show();
            // personalizandoa o corpo do modal
            const coporModal = document.getElementById('corpoModal');
            coporModal.textContent = `${evento}?`
            // selecionando o formulário de confirmação de exclusão
            const formConfirmacaoExclusao = document.getElementById('formConfirmacaoExclusao');
            // aguardando o modal de submit 
            formConfirmacaoExclusao.addEventListener('submit', function(e){
                e.preventDefault();
                formConfirmacaoExclusao.action = `/ingressos/deletar/${idIngresso}/`;
                formConfirmacaoExclusao.submit();
            }); 
        });
    });
}

// Selecionando todos os botões com a tag específicada
document.addEventListener('DOMContentLoaded', function(){
    // Chamando a função de confirmar exclusão
    confirmarExlusão();
})
