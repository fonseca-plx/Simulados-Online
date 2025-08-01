document.addEventListener('DOMContentLoaded', function () {
    const iniciarBtn = document.querySelector('.btn-primary');
    const iniciarCard = document.querySelector('.iniciar-simulado');
    const form = document.querySelector('form');

    iniciarBtn.addEventListener('click', function (event) {
        event.preventDefault();
        iniciarCard.style.display = 'block';
        window.scrollTo({
            top: iniciarCard.offsetTop,
            behavior: 'smooth'
        });
    });

    // Validação do formulário
    if (form) {
        form.addEventListener('submit', function (event) {
            const questoes = document.querySelectorAll('input[type="radio"]');
            const questoesRespondidas = new Set();
            
            questoes.forEach(function (radio) {
                if (radio.checked) {
                    const questaoId = radio.name.replace('questao_', '');
                    questoesRespondidas.add(questaoId);
                }
            });

            const totalQuestoes = new Set();
            questoes.forEach(function (radio) {
                const questaoId = radio.name.replace('questao_', '');
                totalQuestoes.add(questaoId);
            });

            if (questoesRespondidas.size < totalQuestoes.size) {
                event.preventDefault();
                const questoesFaltando = totalQuestoes.size - questoesRespondidas.size;
                alert(`Por favor, responda todas as questões. Ainda faltam ${questoesFaltando} questão(ões).`);
                return false;
            }

            // Confirma o envio
            if (!confirm('Tem certeza que deseja enviar suas respostas? Esta ação não pode ser desfeita.')) {
                event.preventDefault();
                return false;
            }
        });
    }
});