from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from simulado.services.casousosimulado import SimuladoService
from simulado.models import Simulado, Usuario, Questao
from django.core.exceptions import ValidationError
from simulado.utils import Mensagens

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

class CriarSimuladoView(View):
    template_name = 'simulado/sim/form.html'

    def get(self, request):
        """
        Renderiza o formulário para criar um novo simulado.
        """
        if not request.user.is_authenticated:
            return redirect('simulado:login')
        
        # Buscar todas as questões disponíveis para seleção
        questoes_disponiveis = Questao.objects.all().order_by('assunto', 'enunciado')
        
        context = {
            'questoes_disponiveis': questoes_disponiveis
        }
        
        return render(request, self.template_name, context)

    def post(self, request):
        """
        Processa o formulário de criação de simulado.
        """
        if not request.user.is_authenticated:
            return redirect('simulado:login')
        
        tema = request.POST.get('tema')

        # Buscar todas as questões disponíveis para seleção
        questoes_disponiveis = Questao.objects.all().order_by('assunto', 'enunciado')
        
        context = {
            'questoes_disponiveis': questoes_disponiveis
        }
        
        # Obter questões selecionadas pelo usuário
        questoes_selecionadas = request.POST.getlist('questoes')  # Lista de IDs das questões
        
        # Obter pesos definidos pelo usuário para cada questão
        pesos_questoes = {}
        for questao_id in questoes_selecionadas:
            peso_key = f'peso_questao_{questao_id}'
            peso_valor = request.POST.get(peso_key)
            if peso_valor:
                pesos_questoes[questao_id] = peso_valor
        
        try:
            usuario = Usuario.objects.get(id=request.user.id)
        except Usuario.DoesNotExist:
            Mensagens.processar_erros_validacao(
                request, 
                ValidationError("Usuário não encontrado. Faça login novamente.")
            )
            return redirect('simulado:login')
        
        try:
            # Validar se pelo menos 10 questões foram selecionadas
            if len(questoes_selecionadas) < 10:
                raise ValidationError(f"Você deve selecionar pelo menos 10 questões. Selecionadas: {len(questoes_selecionadas)}")
            
            # Converter IDs para inteiros
            questoes_ids = [int(qid) for qid in questoes_selecionadas]
            
            simulado = SimuladoService.criar_simulado(
                tema=tema, 
                usuario=usuario, 
                questoes_ids=questoes_ids,
                pesos_questoes=pesos_questoes
            )
            Mensagens.sucesso(request, f"O simulado sobre {simulado.tema} foi criado com sucesso!")
            return redirect('simulado:detalhar_simulado', simulado_id=simulado.id)
        except ValidationError as e:
            Mensagens.processar_erros_validacao(request, e)
            return render(request, self.template_name, context)
        except ValueError as e:
            Mensagens.processar_erros_validacao(
                request, 
                ValidationError("IDs de questões inválidos fornecidos.")
            )
            return render(request, self.template_name, context)

class CalcularResultadoView(View):
    def get(self, request, *args, **kwargs):
        """
        Redireciona para a página de detalhes do simulado.
        """
        simulado_id = kwargs.get('simulado_id')
        simulado = SimuladoService.buscar_simulados().filter(id=simulado_id).first()
        
        if not simulado:
            return render(request, '404.html', status=404)
        
        return redirect('simulado:detalhar_simulado', simulado_id=simulado.id)

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