from django import forms
from django.core.exceptions import ValidationError
from simulado.models import Usuario

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
        return nome

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("A senha deve ter pelo menos 8 caracteres.")
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("As senhas não coincidem.")
        return cleaned_data
