from django import forms
from django.core.exceptions import ValidationError
from simulado.models import Usuario
import re

class UsuarioForm(forms.Form):
    """Formulário para criação de um novo usuário."""

    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'nome',
            'placeholder': 'Digite seu nome completo'
        }),
        label='Nome Completo'
    )

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'placeholder': 'Digite seu nome de usuário'
        }), 
        label='Nome de usuário'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
            'placeholder': 'Digite sua senha'
        }), 
        label='Senha'
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'confirm_password',
            'placeholder': 'Confirme sua senha'
        }),
        label='Confirmar Senha'
    )

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if not nome:
            raise ValidationError("O nome completo é obrigatório.")
        if len(nome) < 3:
            raise ValidationError('O nome deve ter pelo menos 3 caracteres.')
        return nome

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise ValidationError("Este nome de usuário já está em uso.")
        if len(username) < 3:
            raise ValidationError('O nome de usuário deve ter pelo menos 3 caracteres.')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        erros = []
        
        if len(password) < 6:
            erros.append('A senha deve ter pelo menos 6 caracteres.')
        if not re.search(r'[A-Z]', password):
            erros.append('A senha deve conter pelo menos uma letra maiúscula.')
        if not re.search(r'[a-z]', password):
            erros.append('A senha deve conter pelo menos uma letra minúscula.')
        if not re.search(r'\d', password):
            erros.append('A senha deve conter pelo menos um dígito.')
        if not re.search(r'[@$!%*?&]', password):
            erros.append('A senha deve conter pelo menos um caractere especial.')
        
        if erros:
            raise ValidationError(erros)
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("As senhas não coincidem.")
        return cleaned_data
