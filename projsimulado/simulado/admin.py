from django.contrib import admin
from .models import Usuario, Questao, Alternativa, Simulado, Peso

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Questao)
admin.site.register(Alternativa)
admin.site.register(Simulado)
admin.site.register(Peso)
