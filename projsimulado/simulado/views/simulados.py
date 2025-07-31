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