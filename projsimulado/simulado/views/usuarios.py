from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from simulado.utils import GerenciarSessao, Mensagens

class LoginView(View):
    def get(self, request):
        """
        Renderiza a página de login.
        """
        return render(request, 'simulado/login.html')
    
    def post(self, request):
        """
        Processa o login do usuário.
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('simulado:index')
        else:
            Mensagens.processar_erros_validacao(request, ValidationError("Usuário ou senha inválidos."))
            return render(request, 'simulado/login.html')

class LogoutView(View):
    def get(self, request):
        return self.logout_user(request)

    def post(self, request):
        return self.logout_user(request)

    def logout_user(self, request):
        """
        Realiza o logout do usuário e limpa a sessão.
        """
        GerenciarSessao.limpar_sessao(request)
        logout(request)
        return redirect('simulado:index')