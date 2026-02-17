function cancelarCompra(){
        let botao = document.querySelector('.btnCancelarAlteracoes');
        botao.addEventListener('click', function(){
        window.location.href = '/core/home/';
        });
    }

function confirmarCompra(){
    const formularioCompra = document.getElementById('formularioCompra');
    const modal = document.getElementById('modalConfirmarCompra');
    const modalBootstrap = new bootstrap.Modal(modal);
    formularioCompra.addEventListener('submit', function(event){
        event.preventDefault();
        /* obtendo o botao e a qnt de ingressos */
        const botao = document.getElementById('btnConfirmarCompra');
        const qntIngressos = document.getElementById('id_quantidade').value;
        /* Exibindo o modal */
        modalBootstrap.show();
        /* detalhes do corpo do modal */
        const spanQuantidade = document.getElementById('spanQuantidade');
        const spanEvento = document.getElementById('spanEvento');
        /* personalizando o modal de acordo com o ingresso e quantidade */
        spanQuantidade.innerText = qntIngressos;
        spanEvento.innerText = botao.dataset.evento;
        /* confirmando a compra */
        const formConfirmacaoCompra = document.getElementById('formConfirmacaoCompra');
        formConfirmacaoCompra.addEventListener('submit', function(e){
            e.preventDefault();
            formularioCompra.submit();
        });
    });
}

/* Aguardando toda a página carregar */
document.addEventListener('DOMContentLoaded', function(event){
    /* função que cancela a compra */
    cancelarCompra();
    
    /* função que cofirma a compra*/
    confirmarCompra();
    
});