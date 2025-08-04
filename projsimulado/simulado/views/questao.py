from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from simulado.services.casousoquestao import QuestaoService
from simulado.models import Questao
from django.core.exceptions import ValidationError
from simulado.utils import Mensagens

class ListarQuestoesView(ListView):
    template_name = 'simulado/questoes/lista.html'
    context_object_name = 'questoes'
    paginate_by = 5

    def get_queryset(self):
        """
        Retorna a lista de questões filtrada por assunto e usuário.
        """
        assunto = self.request.GET.get('assunto')
        enunciado = self.request.GET.get('enunciado')
        usuario = self.request.GET.get('usuario')

        return QuestaoService.buscar_questoes(assunto, enunciado, usuario)
    
class CriarQuestaoView(View):
    template_name = 'simulado/questoes/form.html'

    def get(self, request):
        """
        Renderiza o formulário para criar uma nova questão.
        """
        if not request.user.is_authenticated:
            return redirect('simulado:login')
        
        return render(request, self.template_name)

    def post(self, request):
        """
        Processa o formulário de criação de questão.
        """
        enunciado = request.POST.get('enunciado')
        assunto = request.POST.get('assunto')
        usuario = request.user  # Assume que o usuário está autenticado
        alternativas_data = [
            {
                'texto': request.POST.get(f'alternativa_{i}'),
                'correta': request.POST.get(f'correta_{i}') == 'on'
            }
            for i in range(1, 6)  # Espera 5 alternativas
        ]

        # Chamar o serviço para criar a questão
        try:
            QuestaoService.criar_questao(
                enunciado=enunciado,
                assunto=assunto,
                usuario=usuario,
                alternativas_data=alternativas_data
            )
            return redirect('simulado:listar_questoes')
        except ValidationError as e:
            Mensagens.processar_erros_validacao(request, e)
        except Exception as e:
            Mensagens.processar_erros_validacao(request, ValidationError(f"Erro: {str(e)}"))

        return render(request, self.template_name, {
            'enunciado': enunciado,
            'assunto': assunto,
            'alternativas_data': alternativas_data
        })