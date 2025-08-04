from django import template
from django.http import QueryDict

register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    """
    Template tag para manter os parâmetros de busca durante a paginação.
    
    Usage: {% url_replace request 'page' page_number %}
    """
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()

@register.simple_tag(takes_context=True)
def paginator_url(context, page_number):
    """
    Template tag específico para paginação que preserva os parâmetros de busca.
    
    Usage: {% paginator_url page_number %}
    """
    request = context['request']
    query = request.GET.copy()
    query['page'] = page_number
    return '?' + query.urlencode()
