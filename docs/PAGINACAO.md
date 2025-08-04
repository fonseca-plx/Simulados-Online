# Documentação do Sistema de Paginação

## Visão Geral

O sistema de paginação foi implementado no template base (`base.html`) e funciona automaticamente com qualquer view que use `ListView` do Django com paginação habilitada.

## Como Usar

### 1. Configurando uma View com Paginação

Para usar a paginação em uma view, você precisa:

```python
from django.views.generic import ListView

class MinhaListView(ListView):
    model = MeuModel
    template_name = 'meu_template.html'
    context_object_name = 'meus_objetos'
    paginate_by = 10  # Número de itens por página
```

### 2. Template

O template deve estender `base.html` e usar o context_object_name definido na view:

```html
{% extends 'simulado/base.html' %}

{% block content %}
    {% for objeto in meus_objetos %}
        <!-- Conteúdo dos objetos -->
    {% endfor %}
{% endblock %}
```

### 3. Parâmetros Automáticos

O paginador preserva automaticamente os parâmetros de busca da URL. Por exemplo:
- `?tema=django&page=2` - mantém o filtro de tema na página 2
- `?usuario=admin&assunto=python&page=3` - mantém todos os filtros na página 3

## Funcionalidades do Paginador

### Navegação
- **Primeira página** (`<<`): Vai para a página 1
- **Página anterior** (`<`): Vai para a página anterior
- **Números das páginas**: Mostra páginas próximas à atual
- **Próxima página** (`>`): Vai para a próxima página
- **Última página** (`>>`): Vai para a última página

### Características Especiais
- **Reticências**: Aparecem quando há muitas páginas (mostra `...`)
- **Página ativa**: Destacada visualmente
- **Botões desabilitados**: Quando não há página anterior/próxima
- **Contador de resultados**: Mostra "Mostrando X a Y de Z resultados"

### Responsividade
- Em telas pequenas, alguns números de páginas são ocultados
- Mantém os controles essenciais (primeira, anterior, próxima, última)
- Design adaptativo com Bootstrap 5

## Customização

### CSS Personalizado
O arquivo `static/css/pagination.css` contém estilos personalizados que podem ser modificados:

- Cores dos botões
- Efeitos de hover
- Espaçamento e bordas
- Responsividade

### Template Tags Disponíveis

#### `paginator_url`
Preserva parâmetros de busca durante a navegação:
```html
{% paginator_url page_number %}
```

#### `url_replace`
Para substituir qualquer parâmetro mantendo os outros:
```html
{% url_replace request 'page' 2 %}
```

## Exemplos de Uso

### View de Simulados
```python
class ListarSimuladosView(ListView):
    template_name = 'simulado/sim/lista.html'
    context_object_name = 'simulados'
    paginate_by = 5

    def get_queryset(self):
        tema = self.request.GET.get('tema')
        return Simulado.objects.filter(tema__icontains=tema) if tema else Simulado.objects.all()
```

### View de Questões
```python
class ListarQuestoesView(ListView):
    template_name = 'simulado/questoes/lista.html'
    context_object_name = 'questoes'
    paginate_by = 5

    def get_queryset(self):
        assunto = self.request.GET.get('assunto')
        return Questao.objects.filter(assunto__icontains=assunto) if assunto else Questao.objects.all()
```

## Contexto Automático do Django

Quando você usa `ListView` com `paginate_by`, o Django automaticamente fornece:

- `is_paginated`: Boolean indicando se há paginação
- `page_obj`: Objeto da página atual com métodos como:
  - `has_previous()`: Se há página anterior
  - `has_next()`: Se há próxima página
  - `previous_page_number`: Número da página anterior
  - `next_page_number`: Número da próxima página
  - `start_index()`: Índice do primeiro item na página
  - `end_index()`: Índice do último item na página
- `paginator`: Objeto paginador com:
  - `count`: Total de objetos
  - `num_pages`: Total de páginas
  - `page_range`: Range de números das páginas

## Troubleshooting

### Paginação não aparece
1. Verifique se `paginate_by` está definido na view
2. Confirme que há mais objetos que o valor de `paginate_by`
3. Verifique se o template estende `base.html`

### Filtros não são preservados
1. Certifique-se de que está usando `{% paginator_url %}` nos links
2. Verifique se o template carrega `{% load pagination_tags %}`

### Estilos não aparecem
1. Confirme que `{% load static %}` está no template
2. Verifique se o arquivo `pagination.css` existe
3. Execute `python manage.py collectstatic` se necessário
