from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from simulado.utils import GerenciarSessao, Mensagens
from django.contrib import messages
from simulado.forms import UsuarioForm
from simulado.services.casousousuario import UsuarioService

class CadastrarUsuarioView(View):
    def get(self, request):
        """
        Renderiza a página de cadastro de usuário.
        """
        if request.user.is_authenticated:
            return redirect('simulado:index')
        
        form = UsuarioForm()
        return render(request, 'simulado/cadastro.html', {'form': form})

    def post(self, request):
        """
        Processa o cadastro de um novo usuário.
        """
        form = UsuarioForm(request.POST)
        
        if form.is_valid():
            try:
                usuario = UsuarioService.criar_usuario(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    nome=form.cleaned_data['nome']
                )

                usuario = authenticate(
                    request,
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password']
                )

                if usuario:
                    login(request, usuario)
                    messages.success(request, "Usuário cadastrado com sucesso!")
                    return redirect('simulado:index')
                
            except ValidationError as e:
                Mensagens.processar_erros_validacao(request, e)
            except Exception as e:
                Mensagens.processar_erros_validacao(request, ValidationError(f"Erro: {str(e)}"))

        return render(request, 'simulado/cadastro.html', {'form': form})

class LoginView(View):
    def get(self, request):
        """
        Renderiza a página de login.
        """
        if request.user.is_authenticated:
            return redirect('simulado:index')
        
        return render(request, 'simulado/login.html')
    
    def post(self, request):
        """
        Processa o login do usuário.
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user:
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