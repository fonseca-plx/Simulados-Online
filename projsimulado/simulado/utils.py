from django.contrib import messages

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
        # Lista para armazenar mensagens únicas
        mensagens_unicas = set()
        
        if hasattr(validation_error, 'message_dict') and validation_error.message_dict:
            # Erros estruturados por campo
            for campo, erros in validation_error.message_dict.items():
                if isinstance(erros, list):
                    for erro in erros:
                        mensagem = f'{campo.title()}: {erro}'
                        mensagens_unicas.add(mensagem)
                else:
                    mensagem = f'{campo.title()}: {erros}'
                    mensagens_unicas.add(mensagem)

        elif hasattr(validation_error, 'messages') and validation_error.messages:
            # Lista de mensagens de erro
            for mensagem in validation_error.messages:
                mensagens_unicas.add(str(mensagem))
        
        else:
            # Mensagem simples
            mensagens_unicas.add(str(validation_error))
        
        # Adiciona apenas mensagens únicas
        for mensagem in mensagens_unicas:
            messages.error(request, mensagem)
