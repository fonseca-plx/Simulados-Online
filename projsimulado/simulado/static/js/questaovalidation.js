document.addEventListener('DOMContentLoaded', function() {
    // Contador de caracteres para o enunciado
    const enunciadoTextarea = document.getElementById('enunciado');
    const enunciadoCounter = document.getElementById('enunciado-counter');
    
    function updateEnunciadoCounter() {
        const length = enunciadoTextarea.value.length;
        enunciadoCounter.textContent = length;
        
        // Mudança de cor baseada no limite
        const counterElement = enunciadoCounter.parentElement;
        if (length > 900) {
            counterElement.className = 'char-counter mt-1 danger';
        } else if (length > 800) {
            counterElement.className = 'char-counter mt-1 warning';
        } else {
            counterElement.className = 'char-counter mt-1';
        }
    }
    
    enunciadoTextarea.addEventListener('input', updateEnunciadoCounter);
    updateEnunciadoCounter(); // Inicializar contador
    
    // Contador de caracteres para alternativas
    const alternativaInputs = document.querySelectorAll('.alternativa-texto');
    alternativaInputs.forEach(function(input, index) {
        const counter = input.closest('.alternativa-group').querySelector('.alt-counter');
        
        function updateCounter() {
            const length = input.value.length;
            counter.textContent = length;
            
            const counterElement = counter.parentElement;
            if (length > 90) {
                counterElement.className = 'char-counter mt-1 danger';
            } else if (length > 80) {
                counterElement.className = 'char-counter mt-1 warning';
            } else {
                counterElement.className = 'char-counter mt-1';
            }
        }
        
        input.addEventListener('input', updateCounter);
        updateCounter(); // Inicializar contador
    });
    
    // Destacar alternativa correta
    const radioInputs = document.querySelectorAll('input[name="alternativa_correta"]');
    radioInputs.forEach(function(radio) {
        radio.addEventListener('change', function() {
            // Remover destaque de todas as alternativas
            document.querySelectorAll('.alternativa-group').forEach(function(group) {
                group.classList.remove('correta');
            });
            
            // Adicionar destaque à alternativa selecionada
            if (this.checked) {
                this.closest('.alternativa-group').classList.add('correta');
            }
        });
        
        // Verificar estado inicial
        if (radio.checked) {
            radio.closest('.alternativa-group').classList.add('correta');
        }
    });
    
    // Validação do formulário
    const form = document.getElementById('questaoForm');
    form.addEventListener('submit', function(e) {
        let isValid = true;
        let errorMessage = '';
        
        // Verificar enunciado
        const enunciado = enunciadoTextarea.value.trim();
        if (enunciado.length < 10) {
            isValid = false;
            errorMessage += 'O enunciado deve ter pelo menos 10 caracteres.\n';
        }
        
        // Verificar se todas as alternativas estão preenchidas
        let alternativasPreenchidas = 0;
        const textosAlternativas = [];
        
        alternativaInputs.forEach(function(input) {
            const texto = input.value.trim();
            if (texto) {
                alternativasPreenchidas++;
                textosAlternativas.push(texto.toLowerCase());
            }
        });
        
        if (alternativasPreenchidas < 5) {
            isValid = false;
            errorMessage += 'Todas as 5 alternativas devem ser preenchidas.\n';
        }
        
        // Verificar textos duplicados
        const textosUnicos = [...new Set(textosAlternativas)];
        if (textosUnicos.length !== textosAlternativas.length) {
            isValid = false;
            errorMessage += 'Não pode haver alternativas com textos duplicados.\n';
        }
        
        // Verificar se uma alternativa está marcada como correta
        const alternativaCorreta = document.querySelector('input[name="alternativa_correta"]:checked');
        if (!alternativaCorreta) {
            isValid = false;
            errorMessage += 'Selecione uma alternativa como correta.\n';
        }
        
        if (!isValid) {
            e.preventDefault();
            alert('Erro na validação:\n\n' + errorMessage);
        }
    });
    
    // Adicionar evento para sincronizar radio com input hidden
    radioInputs.forEach(function(radio) {
        radio.addEventListener('change', function() {
            // Limpar todos os inputs hidden de correta
            for (let i = 1; i <= 5; i++) {
                const hiddenInput = document.querySelector(`input[name="correta_${i}"]`);
                if (hiddenInput) {
                    hiddenInput.remove();
                }
            }
            
            // Adicionar input hidden para a alternativa selecionada
            if (this.checked) {
                const hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = `correta_${this.value}`;
                hiddenInput.value = 'on';
                form.appendChild(hiddenInput);
            }
        });
    });
});