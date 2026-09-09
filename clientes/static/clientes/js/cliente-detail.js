document.addEventListener('DOMContentLoaded', ()=>{
    const btnConfirmarReset = document.getElementById('btn-confirmar-reset');
    const formReset = document.getElementById('form-reset-senha');

    btnConfirmarReset.addEventListener('click', (event)=>{
        formReset.submit();
    })
})