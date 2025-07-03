from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Usuario(User):
    nome = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['username']

class Questao(models.Model):
    enunciado = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='questoes')

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

    def __str__(self):
        return f'{self.questao.enunciado[:50]} - {self.valor}'

    class Meta:
        verbose_name = 'Peso'
        verbose_name_plural = 'Pesos'
        ordering = ['questao', 'valor']