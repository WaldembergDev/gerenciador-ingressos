function cancelarAlteracoes(){
    let bntCancelar = document.getElementById('bntCancelar');
        bntCancelar.addEventListener('click', function(){
            window.location.href = "/core/home/";
        });
}

document.addEventListener('DOMContentLoaded', function(){
    cancelarAlteracoes();
});

const selectTipoEvento = document.getElementById('id_tipo');
const selectTimeCasa = document.getElementById('id_time_casa');
const selectTimeVisitante = document.getElementById('id_time_visitante');
const titulo = document.getElementById('id_titulo');

selectTipoEvento.addEventListener('change', (event)=>{
    const tipoEvento = event.target.value;

    const nomeTimeCasa = selectTimeCasa.options[selectTimeCasa.selectedIndex].text;    
    const nomeTimeVisitante = selectTimeVisitante.options[selectTimeVisitante.selectedIndex].text;

    titulo.value = nomeTimeCasa;
})