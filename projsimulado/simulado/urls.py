from django.urls import path
from .views.usuarios import *
from .views.index import IndexView
from .views.simulados import *
from .views.questao import *

app_name = 'simulado'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),

    # URL patterns for user authentication
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("cadastrar/", CadastrarUsuarioView.as_view(), name="cadastrar_usuario"),
    
    # URL patterns for simulados
    path("simulados/", ListarSimuladosView.as_view(), name="listar_simulados"),
    path("simulados/<int:simulado_id>/", DetalharSimuladoView.as_view(), name="detalhar_simulado"),
    path("simulados/<int:simulado_id>/resultado/", CalcularResultadoView.as_view(), name="calcular_resultado"),

    # URL patterns for questões
    path("questoes/", ListarQuestoesView.as_view(), name="listar_questoes"),
    path("questoes/criar/", CriarQuestaoView.as_view(), name="criar_questao"),
]