// JavaScript para funcionalidades do formulário de criação de simulado
document.addEventListener('DOMContentLoaded', function() {
    // Elementos da página
    const checkboxes = document.querySelectorAll('input[name="questoes"]');
    const contadorElement = document.getElementById('questoes-selecionadas');
    const progressBar = document.getElementById('progress-questoes');
    const statusElement = document.getElementById('status-simulado');
    const btnCriar = document.getElementById('btn-criar-simulado');
    const btnLimpar = document.getElementById('btn-limpar');
    const form = document.getElementById('simuladoForm');

    // Função para atualizar contador e status
    function atualizarContador() {
        const selecionadas = Array.from(checkboxes).filter(cb => cb.checked);
        const quantidade = selecionadas.length;
        
        if (contadorElement) {
            contadorElement.textContent = quantidade;
        }
        
        // Atualizar progress bar
        if (progressBar) {
            const progresso = Math.min((quantidade / 10) * 100, 100);
            progressBar.style.width = progresso + '%';
            
            if (quantidade >= 10) {
                progressBar.className = 'progress-bar bg-success';
            } else {
                progressBar.className = 'progress-bar bg-warning';
            }
        }
        
        // Atualizar status e botão
        if (statusElement && btnCriar) {
            if (quantidade >= 10) {
                statusElement.innerHTML = '<i class="bi bi-check-circle me-1"></i> Pronto para criar!';
                statusElement.className = 'text-success';
                btnCriar.disabled = false;
            } else {
                const faltam = 10 - quantidade;
                statusElement.innerHTML = `<i class="bi bi-clock me-1"></i> Faltam ${faltam} questões`;
                statusElement.className = 'text-warning';
                btnCriar.disabled = true;
            }
        }
    }

    // Função para configurar input de peso
    function configurarPesoInput(questaoId, habilitado) {
        const pesoInput = document.getElementById(`peso_questao_${questaoId}`);
        if (pesoInput) {
            pesoInput.disabled = !habilitado;
            if (!habilitado) {
                pesoInput.value = '5'; // valor padrão
            } else if (!pesoInput.value || pesoInput.value === '') {
                pesoInput.value = '5'; // valor padrão quando habilita
            }
        }
    }

    // Função para configurar visual do card
    function configurarCardVisual(questaoId, selecionado) {
        const card = document.querySelector(`[data-questao-id="${questaoId}"]`);
        if (card) {
            if (selecionado) {
                card.classList.add('selected');
            } else {
                card.classList.remove('selected');
            }
        }
    }

    // Event listeners para checkboxes
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const questaoId = this.value;
            const selecionado = this.checked;
            
            configurarPesoInput(questaoId, selecionado);
            configurarCardVisual(questaoId, selecionado);
            atualizarContador();
        });
        
        // Configurar estado inicial
        const questaoId = checkbox.value;
        const selecionado = checkbox.checked;
        configurarPesoInput(questaoId, selecionado);
        configurarCardVisual(questaoId, selecionado);
    });

    // Event listener para botão limpar
    if (btnLimpar) {
        btnLimpar.addEventListener('click', function(e) {
            e.preventDefault();
            
            checkboxes.forEach(checkbox => {
                checkbox.checked = false;
                const questaoId = checkbox.value;
                configurarPesoInput(questaoId, false);
                configurarCardVisual(questaoId, false);
            });
            
            // Limpar também o campo tema
            const temaInput = document.getElementById('tema');
            if (temaInput) {
                temaInput.value = '';
            }
            
            atualizarContador();
        });
    }

    // Validação em tempo real do campo tema
    const temaInput = document.getElementById('tema');
    if (temaInput) {
        temaInput.addEventListener('input', function() {
            const valor = this.value.trim();
            const feedbackDiv = this.parentNode.querySelector('.invalid-feedback') || 
                               this.parentNode.querySelector('.tema-feedback');
            
            // Remove feedback anterior
            if (feedbackDiv) {
                feedbackDiv.remove();
            }
            
            // Validação
            let mensagem = '';
            if (valor.length > 0 && valor.length < 5) {
                mensagem = 'O tema deve ter pelo menos 5 caracteres.';
                this.classList.add('is-invalid');
            } else if (valor.length > 30) {
                mensagem = 'O tema não pode ter mais de 30 caracteres.';
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
                if (valor.length >= 5) {
                    this.classList.add('is-valid');
                } else {
                    this.classList.remove('is-valid');
                }
            }
            
            // Adiciona mensagem de erro se necessário
            if (mensagem) {
                const feedback = document.createElement('div');
                feedback.className = 'invalid-feedback tema-feedback';
                feedback.textContent = mensagem;
                this.parentNode.appendChild(feedback);
            }
        });
    }

    // Validação dos inputs de peso em tempo real
    document.addEventListener('input', function(e) {
        if (e.target.name && e.target.name.startsWith('peso_questao_')) {
            const valor = parseInt(e.target.value);
            
            if (isNaN(valor) || valor < 1 || valor > 10) {
                e.target.classList.add('is-invalid');
            } else {
                e.target.classList.remove('is-invalid');
                e.target.classList.add('is-valid');
            }
        }
    });

    // Validação antes do submit
    if (form) {
        form.addEventListener('submit', function(e) {
            let erros = [];
            
            // Validar tema
            const tema = document.getElementById('tema').value.trim();
            if (!tema) {
                erros.push('O tema é obrigatório.');
            } else if (tema.length < 5) {
                erros.push('O tema deve ter pelo menos 5 caracteres.');
            } else if (tema.length > 30) {
                erros.push('O tema não pode ter mais de 30 caracteres.');
            }
            
            // Validar questões selecionadas
            const selecionadas = Array.from(checkboxes).filter(cb => cb.checked);
            if (selecionadas.length < 10) {
                erros.push(`Você deve selecionar pelo menos 10 questões. Selecionadas: ${selecionadas.length}`);
            }

            // Verificar se todos os pesos foram preenchidos corretamente
            let pesoInvalido = false;
            let pesosComErro = [];
            
            selecionadas.forEach(checkbox => {
                const pesoInput = document.getElementById(`peso_questao_${checkbox.value}`);
                const peso = parseInt(pesoInput.value);
                
                if (isNaN(peso) || peso < 1 || peso > 10) {
                    pesoInvalido = true;
                    pesosComErro.push(checkbox.value);
                }
            });

            if (pesoInvalido) {
                erros.push('Todos os pesos devem estar entre 1 e 10.');
            }

            // Se houver erros, impedir submit e mostrar mensagens
            if (erros.length > 0) {
                e.preventDefault();
                
                // Criar mensagem de erro
                let mensagem = 'Corrija os seguintes erros:\n\n';
                erros.forEach((erro, index) => {
                    mensagem += `${index + 1}. ${erro}\n`;
                });
                
                alert(mensagem);
                
                // Destacar campos com erro
                if (pesosComErro.length > 0) {
                    pesosComErro.forEach(questaoId => {
                        const pesoInput = document.getElementById(`peso_questao_${questaoId}`);
                        if (pesoInput) {
                            pesoInput.classList.add('is-invalid');
                            pesoInput.focus();
                        }
                    });
                }
                
                return false;
            }
            
            // Mostrar loading no botão
            if (btnCriar) {
                btnCriar.disabled = true;
                btnCriar.innerHTML = '<i class="spinner-border spinner-border-sm me-2"></i>Criando...';
            }
        });
    }

    // Configurar estado inicial
    atualizarContador();
    
    // Melhorar acessibilidade - permitir seleção com Enter/Space nos cards
    document.querySelectorAll('.questao-card').forEach(card => {
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const checkbox = this.querySelector('input[type="checkbox"]');
                if (checkbox) {
                    checkbox.checked = !checkbox.checked;
                    checkbox.dispatchEvent(new Event('change'));
                }
            }
        });
        
        // Tornar o card focável
        card.setAttribute('tabindex', '0');
    });

    // Scroll suave para questões selecionadas
    function scrollToQuestao(questaoId) {
        const card = document.querySelector(`[data-questao-id="${questaoId}"]`);
        if (card) {
            card.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
        }
    }

    // Auto-scroll quando selecionar primeira questão
    let primeiraSelecao = true;
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked && primeiraSelecao) {
                primeiraSelecao = false;
                setTimeout(() => {
                    scrollToQuestao(this.value);
                }, 100);
            }
        });
    });
});
