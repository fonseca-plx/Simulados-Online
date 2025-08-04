from django.shortcuts import get_object_or_404
from simulado.models import Simulado, Peso

class SimuladoService:
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