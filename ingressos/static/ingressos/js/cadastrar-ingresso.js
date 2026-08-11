function cancelarAlteracoes(){
    let bntCancelar = document.getElementById('bntCancelar');
        bntCancelar.addEventListener('click', function(){
            window.location.href = "/core/home/";
        });
}

/* Atualizar Título */
function atualizarTitulo(input){
    input.addEventListener('change', (event)=>{
        const selectTipoEvento = document.getElementById('id_tipo');
        const selectTimeCasa = document.getElementById('id_time_casa');
        const selectTimeVisitante = document.getElementById('id_time_visitante');
        const titulo = document.getElementById('id_titulo');

        const tipoEvento = event.target.value;

        if (selectTimeCasa.value !== "" && selectTimeVisitante.value !== ""){
            const nomeTimeCasa = selectTimeCasa.options[selectTimeCasa.selectedIndex].text;
            const nomeTimeVisitante = selectTimeVisitante.options[selectTimeVisitante.selectedIndex].text;
            titulo.value = `${nomeTimeCasa} vs ${nomeTimeVisitante}`;
        }

    })
}

function atualizar(){
    const selectTipoEvento = document.getElementById('id_tipo');
    const selectTimeCasa = document.getElementById('id_time_casa');
    const selectTimeVisitante = document.getElementById('id_time_visitante');

    atualizarTitulo(selectTipoEvento);
    atualizarTitulo(selectTimeCasa);
    atualizarTitulo(selectTimeVisitante);
}

function esconderTimes(){
    const selectTipoEvento = document.getElementById('id_tipo');
    const selectTimeCasa = document.getElementById('id_time_casa');
    const selectTimeVisitante = document.getElementById('id_time_visitante');
    const divTimeCasa = document.getElementById('div-time-casa');
    const divTimeVisitante = document.getElementById('div-time-visitante');
    
    selectTipoEvento.addEventListener('change', (event)=>{
        tipoEvento = event.target.value;
        if (tipoEvento == 'SHOW'){
            divTimeCasa.style.display = 'none';
            divTimeVisitante.style.display = 'none';   
            selectTimeCasa.value = "";
            selectTimeVisitante.value = "";
        }else{
            divTimeCasa.style.display = 'block';
            divTimeVisitante.style.display = 'block';
        }
        
    })
}

document.addEventListener('DOMContentLoaded', function(){
    cancelarAlteracoes();
    atualizar();
    esconderTimes();
});






