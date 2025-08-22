// Sistema de mensagens automáticas
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(function(alert) {
        // Verificar se é mensagem de sucesso ou info para auto-dismiss
        const isAutoClose = alert.classList.contains('alert-success') || 
                           alert.classList.contains('alert-info');
        
        // Auto-dismiss APENAS para mensagens de sucesso e info
        if (isAutoClose) {
            setTimeout(function() {
                if (alert && alert.parentElement) {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                }
            }, 5000); // 5 segundos
        }
        
        // Adicionar animação suave para TODAS as mensagens
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-20px)';
        
        setTimeout(function() {
            alert.style.transition = 'all 0.3s ease-in-out';
            alert.style.opacity = '1';
            alert.style.transform = 'translateY(0)';
        }, 100);
    });
});

// Função para criar mensagens dinamicamente via JavaScript
function showMessage(type, message, autoClose = null) {
    const container = document.querySelector('.messages-container') || 
                     document.querySelector('.container');
    
    if (!container) return;
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    
    const icons = {
        'success': 'bi-check-circle',
        'error': 'bi-exclamation-triangle',
        'danger': 'bi-exclamation-triangle',
        'warning': 'bi-exclamation-circle',
        'info': 'bi-info-circle'
    };
    
    const icon = icons[type] || 'bi-info-circle';
    
    alertDiv.innerHTML = `
        <i class="bi ${icon} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
    `;
    
    container.insertBefore(alertDiv, container.firstChild);
    
    // Determinar auto-close baseado no tipo de mensagem
    const shouldAutoClose = autoClose !== null ? autoClose : (type === 'success' || type === 'info');
    
    // Auto-close apenas para success e info (ou se explicitamente definido)
    if (shouldAutoClose) {
        setTimeout(function() {
            if (alertDiv && alertDiv.parentElement) {
                const bsAlert = new bootstrap.Alert(alertDiv);
                bsAlert.close();
            }
        }, 5000);
    }
    
    // Adicionar animação para a nova mensagem
    alertDiv.style.opacity = '0';
    alertDiv.style.transform = 'translateY(-20px)';
    
    setTimeout(function() {
        alertDiv.style.transition = 'all 0.3s ease-in-out';
        alertDiv.style.opacity = '1';
        alertDiv.style.transform = 'translateY(0)';
    }, 100);
}

// Função para mostrar diferentes tipos de mensagens
function showSuccess(message, autoClose = true) {
    showMessage('success', message, autoClose);
}

function showError(message, autoClose = false) {
    showMessage('danger', message, autoClose);
}

function showWarning(message, autoClose = false) {
    showMessage('warning', message, autoClose);
}

function showInfo(message, autoClose = true) {
    showMessage('info', message, autoClose);
}