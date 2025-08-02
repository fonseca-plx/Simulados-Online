from django.urls import path
from .views.usuarios import LoginView, LogoutView
from .views.index import IndexView
from .views.simulados import ListarSimuladosView, DetalharSimuladoView, CalcularResultadoView

app_name = 'simulado'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),

    # URL patterns for user authentication
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    
    # URL patterns for simulados
    path("simulados/", ListarSimuladosView.as_view(), name="listar_simulados"),
    path("simulados/<int:simulado_id>/", DetalharSimuladoView.as_view(), name="detalhar_simulado"),
    path("simulados/<int:simulado_id>/resultado/", CalcularResultadoView.as_view(), name="calcular_resultado"),
]