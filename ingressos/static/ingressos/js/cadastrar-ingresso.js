function cancelarAlteracoes(){
    let bntCancelar = document.getElementById('bntCancelar');
        bntCancelar.addEventListener('click', function(){
            window.location.href = "/core/home/";
        });
}

document.addEventListener('DOMContentLoaded', function(){
    cancelarAlteracoes();
});

