from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError
from simulado.models import Simulado, Peso, Questao

class SimuladoService:
    @staticmethod
    def criar_simulado(tema, usuario, questoes_ids, pesos_questoes):
        """
        Cria um novo simulado com um tema, usuário e questões.
        
        Args:
            tema: Tema do simulado
            usuario: Usuário que está criando o simulado
            questoes_ids: Lista de IDs de questões escolhidas
            pesos_questoes: Dicionário com questao_id: peso_valor (cada questão deve ter um peso)
        
        Returns:
            Simulado criado ou None em caso de erro
        
        Raises:
            ValidationError: Se as validações falharem
        """
        # Validações iniciais
        erros = {}
        
        # Validar parâmetros obrigatórios
        if not tema:
            erros['tema'] = 'O tema é obrigatório.'
        if not usuario:
            erros['usuario'] = 'O usuário é obrigatório.'
        if not questoes_ids:
            erros['questoes'] = 'Pelo menos uma questão deve ser selecionada.'
        if not pesos_questoes:
            erros['pesos'] = 'Os pesos das questões são obrigatórios.'
        
        # Validar quantidade mínima de questões
        if questoes_ids and len(questoes_ids) < 10:
            erros['questoes'] = f'Você deve selecionar pelo menos 10 questões. Selecionadas: {len(questoes_ids)}'
        
        # Verificar se todas as questões existem
        if questoes_ids:
            questoes_existentes = Questao.objects.filter(id__in=questoes_ids)
            if questoes_existentes.count() != len(questoes_ids):
                questoes_inexistentes = set(questoes_ids) - set(questoes_existentes.values_list('id', flat=True))
                erros['questoes'] = f'As seguintes questões não existem: {list(questoes_inexistentes)}'
        
        # Validar se todos os pesos foram fornecidos
        if questoes_ids and pesos_questoes:
            for questao_id in questoes_ids:
                questao_id_str = str(questao_id)
                if questao_id_str not in pesos_questoes:
                    erros['pesos'] = f'Peso não fornecido para a questão ID: {questao_id}'
                    break
                else:
                    try:
                        peso_valor = int(pesos_questoes[questao_id_str])
                        if peso_valor < 1 or peso_valor > 10:
                            erros['pesos'] = f'O peso da questão {questao_id} deve estar entre 1 e 10. Valor fornecido: {peso_valor}'
                            break
                    except (ValueError, TypeError):
                        erros['pesos'] = f'Peso inválido para a questão {questao_id}: {pesos_questoes[questao_id_str]}'
                        break
        
        if erros:
            raise ValidationError(erros)
        
        # Criar o simulado usando transação para garantir consistência
        with transaction.atomic():
            # Criar o simulado
            simulado = Simulado(
                tema=tema,
                usuario=usuario
            )
            simulado.save()  # O método save já chama full_clean() que faz as validações do modelo
            
            # Criar os pesos para cada questão
            pesos_para_criar = []
            for questao_id in questoes_ids:
                questao = get_object_or_404(Questao, id=questao_id)
                peso_valor = int(pesos_questoes[str(questao_id)])
                
                peso = Peso(
                    valor=peso_valor,
                    questao=questao,
                    simulado=simulado
                )
                pesos_para_criar.append(peso)
            
            # Validar e salvar todos os pesos
            for peso in pesos_para_criar:
                peso.save()  # O método save já chama full_clean() que faz as validações do modelo
        
        return simulado

    @staticmethod
    def buscar_simulados(tema=None, data_criacao=None, usuario=None):
        """
        Busca simulados com base nos critérios fornecidos.
        """
        simulados = Simulado.objects.all()
        
        if tema:
            simulados = simulados.filter(tema__icontains=tema)
        if data_criacao:
            simulados = simulados.filter(data_criacao__date=data_criacao)
        if usuario:
            simulados = simulados.filter(usuario__username=usuario)
        
        return simulados
    
    @staticmethod
    def calcular_resultado(simulado_id, respostas):
        """
        Calcula o resultado do simulado com base nas respostas fornecidas.
        Inclui o cálculo da pontuação considerando os pesos de cada questão.
        
        Args:
            simulado_id: ID do simulado
            respostas: Dicionário com questao_id: alternativa_id
        """
        simulado = get_object_or_404(Simulado, id=simulado_id)
        questoes = simulado.questoes.all()
        
        acertos = 0
        pontuacao = 0
        detalhes = []
        
        for questao in questoes:
            resposta_correta = questao.alternativas.filter(correta=True).first()
            resposta_usuario_id = respostas.get(str(questao.id))
            
            acertou = False
            if resposta_correta and resposta_usuario_id:
                if str(resposta_correta.id) == str(resposta_usuario_id):
                    acertos += 1
                    acertou = True
                    # Busca o peso da questão para este simulado específico
                    peso = Peso.objects.filter(questao=questao, simulado=simulado).first()
                    if peso:
                        pontuacao += peso.valor
            
            # Adiciona detalhes da resposta para o resultado
            resposta_usuario = None
            if resposta_usuario_id:
                resposta_usuario = questao.alternativas.filter(id=resposta_usuario_id).first()
            
            detalhes.append({
                'questao': questao,
                'resposta_correta': resposta_correta,
                'resposta_usuario': resposta_usuario,
                'acertou': acertou
            })
        
        total_questoes = questoes.count()
        resultado = {
            'simulado': simulado,
            'acertos': acertos,
            'total_questoes': total_questoes,
            'porcentagem': (acertos / total_questoes) * 100 if total_questoes > 0 else 0,
            'pontuacao': pontuacao,
            'detalhes': detalhes
        }
        
        return resultado