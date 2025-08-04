from simulado.models import Usuario, Simulado, Questao, Alternativa
from django.core.exceptions import ValidationError
from django.db import transaction

class QuestaoService:
    @staticmethod
    def criar_questao(enunciado, assunto, usuario, alternativas_data):
        """
        Cria uma nova questão com suas alternativas.
        
        Args:
            enunciado (str): O enunciado da questão
            assunto (str): O assunto da questão
            usuario (Usuario): O usuário que está criando a questão
            alternativas_data (list): Lista de dicionários com dados das alternativas
                                    Cada dicionário deve ter 'texto' e 'correta' (boolean)
        
        Returns:
            Questao: A questão criada
            
        Raises:
            ValidationError: Se houver erros de validação
        """
        # Validação da quantidade de alternativas
        if not alternativas_data or len(alternativas_data) != 5:
            raise ValidationError({
                'alternativas': 'Uma questão deve ter exatamente 5 alternativas.'
            })
        
        # Validação de alternativas corretas
        alternativas_corretas = [alt for alt in alternativas_data if alt.get('correta', False)]
        if len(alternativas_corretas) != 1:
            raise ValidationError({
                'alternativas': 'Uma questão deve ter exatamente 1 alternativa correta.'
            })
        
        # Validação de textos das alternativas
        textos_alternativas = [alt.get('texto', '').strip() for alt in alternativas_data]
        
        # Verificar se há textos vazios
        if any(not texto for texto in textos_alternativas):
            raise ValidationError({
                'alternativas': 'Todas as alternativas devem ter texto.'
            })
        
        # Verificar se há textos duplicados
        if len(set(textos_alternativas)) != len(textos_alternativas):
            raise ValidationError({
                'alternativas': 'Não pode haver alternativas com textos duplicados.'
            })
        
        # Usar transação para garantir consistência
        try:
            with transaction.atomic():
                # Criar a questão
                questao = Questao(
                    enunciado=enunciado,
                    assunto=assunto,
                    usuario=usuario
                )
                questao.save()
                
                # Criar as alternativas
                for alt_data in alternativas_data:
                    alternativa = Alternativa(
                        texto=alt_data['texto'].strip(),
                        correta=alt_data.get('correta', False),
                        questao=questao
                    )
                    alternativa.save()
                
                # Validar as alternativas após todas serem criadas
                questao.validar_alternativas()
                
                return questao
                
        except ValidationError as e:
            # Re-raise validation errors
            raise e
        except Exception as e:
            # Capturar outros erros e converter para ValidationError
            raise ValidationError({
                'questao': f'Erro ao criar questão: {str(e)}'
            })

    @staticmethod
    def buscar_questoes(assunto=None, enunciado=None, usuario=None):
        """
        Busca questões com base nos filtros fornecidos.
        """
        queryset = Questao.objects.all()
        
        if assunto:
            queryset = queryset.filter(assunto__icontains=assunto)
        if enunciado:
            queryset = queryset.filter(enunciado__icontains=enunciado)
        if usuario:
            queryset = queryset.filter(usuario__username=usuario)
        
        return queryset