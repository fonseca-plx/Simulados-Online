from django.contrib import messages
from django.core.exceptions import ValidationError

class GerenciarSessao:
    @staticmethod
    def limpar_sessao(request):
        """
        Limpa a sessão do usuário, removendo todas as chaves.
        """
        if request.user.is_authenticated:
            request.session.flush()

class Mensagens():
    @staticmethod
    def processar_erros_validacao(request, validation_error):
        """
        Processa erros de validação e adiciona mensagens apropriadas.
        """
        mensagens_unicas = set()
        
        if hasattr(validation_error, 'message_dict') and validation_error.message_dict:
            # Erros estruturados por campo
            for campo, erros in validation_error.message_dict.items():
                if isinstance(erros, list):
                    for erro in erros:
                        mensagem = f'{campo.replace("_", " ").title()}: {erro}'
                        mensagens_unicas.add(mensagem)
                else:
                    mensagem = f'{campo.replace("_", " ").title()}: {erros}'
                    mensagens_unicas.add(mensagem)

        elif hasattr(validation_error, 'messages') and validation_error.messages:
            # Lista de mensagens de erro
            for mensagem in validation_error.messages:
                mensagens_unicas.add(str(mensagem))
        
        else:
            # Mensagem simples
            mensagens_unicas.add(str(validation_error))
        
        # Adiciona mensagens únicas como erro
        for mensagem in mensagens_unicas:
            messages.error(request, mensagem)
    
    @staticmethod
    def sucesso(request, mensagem):
        """Adiciona mensagem de sucesso."""
        messages.success(request, mensagem)
    
    @staticmethod
    def aviso(request, mensagem):
        """Adiciona mensagem de aviso."""
        messages.warning(request, mensagem)
    
    @staticmethod
    def info(request, mensagem):
        """Adiciona mensagem de informação."""
        messages.info(request, mensagem)
    
    @staticmethod
    def debug(request, mensagem):
        """Adiciona mensagem de debug."""
        messages.debug(request, mensagem)
