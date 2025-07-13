from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

# Create your models here.

class Usuario(User):
    nome = models.CharField(max_length=50)

    def clean(self):
        erros = {}
        if len(self.nome) < 3:
            erros['nome'] = 'O nome deve ter pelo menos 3 caracteres.'
        if len(self.username) < 3:
            erros['username'] = 'O nome de usuário deve ter pelo menos 3 caracteres.'
        if len(self.password) < 6:
            erros['password'] = 'A senha deve ter pelo menos 6 caracteres.'
        if not re.search(r'[A-Z]', self.password):
            erros['password'] = 'A senha deve conter pelo menos uma letra maiúscula.'
        if not re.search(r'[a-z]', self.password):
            erros['password'] = 'A senha deve conter pelo menos uma letra minúscula.'
        if not re.search(r'\d', self.password):
            erros['password'] = 'A senha deve conter pelo menos um dígito.'
        if not re.search(r'[@$!%*?&]', self.password):
            erros['password'] = 'A senha deve conter pelo menos um caractere especial.'
        
        if erros:
            raise ValidationError(erros)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['username']

class Questao(models.Model):
    enunciado = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='questoes')

    def clean(self):
        if len(self.enunciado) < 10:
            raise ValidationError({'enunciado': 'O enunciado deve ter pelo menos 10 caracteres.'})
        if len(self.enunciado) > 150:
            raise ValidationError({'enunciado': 'O enunciado não pode ter mais de 150 caracteres.'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.enunciado[:50]  # Retorna os primeiros 50 caracteres do enunciado

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'
        ordering = ['enunciado']

class Alternativa(models.Model):
    texto = models.TextField()
    correta = models.BooleanField(default=False)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name='alternativas')

    def clean(self):
        erros = {}
        if len(self.texto) > 100:
            erros['texto'] = 'O texto da alternativa não pode ter mais de 100 caracteres.'
        if self.questao.alternativas.filter(texto=self.texto).exclude(id=self.id).exists():
            erros['texto'] = 'Já existe uma alternativa com este texto para esta questão.'
        if not self.questao:
            erros['questao'] = 'A alternativa deve estar associada a uma questão.'
        if self.correta and self.questao.alternativas.filter(correta=True).exclude(id=self.id).exists():
            erros['correta'] = 'Já existe uma alternativa correta para esta questão.'
        if not self.correta and not self.questao.alternativas.filter(correta=True).exists():
            erros['correta'] = 'Pelo menos uma alternativa deve ser marcada como correta para esta questão.'        
        
        if erros:
            raise ValidationError(erros)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.texto[:50]  # Retorna os primeiros 50 caracteres do texto

    class Meta:
        verbose_name = 'Alternativa'
        verbose_name_plural = 'Alternativas'
        ordering = ['questao', 'texto']

class Simulado(models.Model):
    tema = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    questoes = models.ManyToManyField(Questao, related_name='simulados', through='Peso')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='simulados')

    def clean(self):
        erros = {}
        if len(self.tema) < 5:
            erros['tema'] = 'O tema deve ter pelo menos 5 caracteres.'
        if len(self.tema) > 30:
            erros['tema'] = 'O tema não pode ter mais de 30 caracteres.'
        if self.questoes.count() < 10:
            erros['questoes'] = 'O simulado deve conter pelo menos 10 questões.'
        if self.questoes.count() > 90:
            erros['questoes'] = 'O simulado não pode conter mais de 90 questões.'
        if not self.usuario:
            erros['usuario'] = 'O simulado deve estar associado a um usuário.'
        
        if erros:
            raise ValidationError(erros)
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Simulado sobre: {self.tema} - Criado em: {self.data_criacao.strftime("%d-%m-%Y %H:%M:%S")}'

    class Meta:
        verbose_name = 'Simulado'
        verbose_name_plural = 'Simulados'
        ordering = ['-data_criacao']

class Peso(models.Model):
    valor = models.IntegerField()
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name='pesos')
    simulado = models.ForeignKey(Simulado, on_delete=models.CASCADE, related_name='pesos')

    def clean(self):
        erros = {}
        if self.valor < 1:
            erros['valor'] = 'O valor do peso deve ser pelo menos 1.'
        if self.valor > 10:
            erros['valor'] = 'O valor do peso não pode ser maior que 10.'
        if not self.questao:
            erros['questao'] = 'O peso deve estar associado a uma questão.'
        if not self.simulado:
            erros['simulado'] = 'O peso deve estar associado a um simulado.'
        
        if erros:
            raise ValidationError(erros)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.questao.enunciado[:50]} - {self.valor}'

    class Meta:
        verbose_name = 'Peso'
        verbose_name_plural = 'Pesos'
        ordering = ['questao', 'valor']