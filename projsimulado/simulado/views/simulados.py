from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from simulado.services.casousosimulado import SimuladoService
from simulado.models import Simulado

class ListarSimuladosView(ListView):
    template_name = 'simulado/sim/lista.html'
    context_object_name = 'simulados'
    paginate_by = 5

    def get_queryset(self):
        """
        Retorna a lista de simulados filtrada por tema, data de criação e usuário.
        """
        tema = self.request.GET.get('tema')
        data_criacao = self.request.GET.get('data_criacao')
        usuario = self.request.GET.get('usuario')

        return SimuladoService.buscar_simulados(tema, data_criacao, usuario)

class DetalharSimuladoView(DetailView):
    model = Simulado
    template_name = 'simulado/sim/detalhe.html'
    context_object_name = 'simulado'
    pk_url_kwarg = 'simulado_id'

class CalcularResultadoView(View):
    def post(self, request, *args, **kwargs):
        """
        Calcula o resultado do simulado com base nas respostas fornecidas.
        """
        simulado_id = kwargs.get('simulado_id')
        
        # Extrai as respostas do formulário
        # As respostas chegam no formato: questao_1: '15', questao_2: '20', etc.
        respostas = {}
        for key, value in request.POST.items():
            if key.startswith('questao_'):
                questao_id = key.replace('questao_', '')
                respostas[questao_id] = value

        resultado = SimuladoService.calcular_resultado(simulado_id, respostas)

        return render(request, 'simulado/sim/resultado.html', {'resultado': resultado})