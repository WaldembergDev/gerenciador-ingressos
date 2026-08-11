let modal = document.getElementById('confirmacaoCadastro');
let tituloModal = document.getElementById('id_titulo');
let localModal = document.getElementById('id_local');
let dataHorarioModal = document.getElementById('id_data_horario');
let descricaoModal = document.getElementById('id_descricao');
let precoModal = document.getElementById('id_preco');
let precoParModal = document.getElementById('id_preco_par');

modal.addEventListener('show.bs.modal', (event) => {
    // Obtendo as variaveis
    /** @type {HTMLButtonElement} */
    let botao = event.relatedTarget;
    let tituloBotao = botao.getAttribute('data-titulo');
    let dataHorarioBotao = botao.getAttribute('data-evento-dia').replace(' ', 'T');
    let campeonatoBotao = botao.getAttribute('data-campeonato');
    
    localModal.value = 'Maracanã';
    tituloModal.value = tituloBotao;
    dataHorarioModal.value = dataHorarioBotao;
    descricaoModal.value = campeonatoBotao;
    precoModal.value = 60.00;
    precoParModal.value = 80;
});

let formModal = document.getElementById('formModal');
let timeCasa = document.getElementById('id_time_casa');
let timeVisitante = document.getElementById('id_time_visitante');
let spanTimeCasa = document.getElementById('span-time-casa');
let spanTimeVisitante = document.getElementById('span-time-visitante');

formModal.addEventListener('submit', (event) => {
    event.preventDefault();

    if (timeCasa.value === "") {
        spanTimeCasa.textContent = 'O time deve ser selecionado';
    }
    if (timeVisitante.value === "") {
        spanTimeCasa = "O time deve ser selecionado";
    }

    if (timeCasa.value === timeVisitante.value) {
        spanTimeVisitante.textContent = "O time visitante deve ser diferente do time casa";
    }

    if (timeCasa.value !== "" && timeVisitante.value !== "" && timeCasa.value !== timeVisitante.value) {
        formModal.submit();
    }
})