from django import template

register = template.Library()

@register.filter(name="limpar_especiais")
def limpar_especiais(telefone):
    telefone_formatado = [char for char in telefone if char.isdigit()]
    telefone_formatado = ''.join(telefone_formatado)
    return telefone_formatado