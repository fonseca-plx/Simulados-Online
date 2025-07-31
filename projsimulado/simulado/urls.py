from django.urls import path
from .views.index import IndexView
from .views.simulados import ListarSimuladosView, DetalharSimuladoView

app_name = 'simulado'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("simulados/", ListarSimuladosView.as_view(), name="listar_simulados"),
    path("simulados/<int:simulado_id>/", DetalharSimuladoView.as_view(), name="detalhar_simulado"),
]