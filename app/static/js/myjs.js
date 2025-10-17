const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const resultsContainer = document.getElementById('results-container');

const modalOverlay = document.getElementById('modal-overlay');
const modalForm = document.getElementById('modal-form');
const cancelButton = document.getElementById('modal-cancel');

let pendingFiles = null;

dropZone.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
});

dropZone.addEventListener('drop', (e) => {
    handleFiles(e.dataTransfer.files);
}, false);

function handleFiles(files) {
    if (files.length === 0) return;
    pendingFiles = files;
    modalOverlay.style.display = 'flex';
}

modalForm.addEventListener('submit', (e) => {
    e.preventDefault();

    // 1. Pega o valor único do radio button selecionado
    const selectedMes = document.querySelector('input[name="mes"]:checked');
    const selectedAno = document.querySelector('input[name="ano"]:checked');

    // 2. Pega TODOS os checkboxes de operação e cria um objeto de status
    const operacoesStatus = {};
    const allOperacoes = document.querySelectorAll('input[name="tipo_operacao"]');
    allOperacoes.forEach(checkbox => {
        // A chave é o 'value' do checkbox, e o valor é '1' se marcado, '0' se não.
        operacoesStatus[checkbox.value] = checkbox.checked ? '1' : '0';
    });

    // 3. Validação: Verifica se Mês e Ano estão selecionados.
    if (!selectedMes || !selectedAno) {
        alert('Por favor, selecione uma opção para Mês e Ano.');
        return;
    }

    modalOverlay.style.display = 'none';
    modalForm.reset();

    // 4. Envia o valor de Mês/Ano e o objeto de status das operações
    performUpload(pendingFiles, selectedMes.value, selectedAno.value, operacoesStatus);
});

cancelButton.addEventListener('click', () => {
    modalOverlay.style.display = 'none';
    modalForm.reset();
    pendingFiles = null;
});

function performUpload(files, mes, ano, operacoes) {
    resultsContainer.innerHTML = '';
    const formData = new FormData();
    
    // Adiciona os dados do modal ao FormData
    formData.append('mes', mes);
    formData.append('ano', ano);
    
    // Adiciona cada operação como um campo separado no FormData
    for (const [operacao, status] of Object.entries(operacoes)) {
        formData.append(operacao, status);
    }

    for (const file of files) {
        formData.append('xml_files[]', file);
    }

    const csrftoken = getCookie('csrftoken');
    dropZone.textContent = 'Processando arquivos...';

    fetch('', {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Dados recebidos pelo servidor:', data.dados_recebidos);
        displayResults(data.results);
        dropZone.textContent = 'Arraste e solte arquivos XML aqui ou clique para selecionar.';
    })
    .catch(error => {
        console.error('Erro:', error);
        resultsContainer.innerHTML = `<div class="result-card error-card"><p class="error-message">Ocorreu um erro no servidor.</p></div>`;
        dropZone.textContent = 'Arraste e solte arquivos XML aqui ou clique para selecionar.';
    });
}

function displayResults(results) {
    if (!results || results.length === 0) return;
    results.forEach(result => {
        const card = document.createElement('div');
        card.classList.add('result-card');
        let cardContent = `<h4>Arquivo: ${result.filename}</h4>`;
        if (result.success) {
            card.classList.add('success-card');
            cardContent += `
                <p><strong>Status:</strong> ${result.xml_content}</p>
            `;
        } else {
            card.classList.add('error-card');
            cardContent += `<p class="error-message">Erro: ${result.error}</p>`;
        }
        card.innerHTML = cardContent;
        resultsContainer.appendChild(card);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function escapeHtml(unsafe) {
    return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
}