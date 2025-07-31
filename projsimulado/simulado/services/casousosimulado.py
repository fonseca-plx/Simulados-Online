from simulado.models import Simulado

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
            simulados = simulados.filter(usuario=usuario)
        
        return simulados