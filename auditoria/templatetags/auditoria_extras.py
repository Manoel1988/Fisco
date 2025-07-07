from django import template
import markdown
import bleach

register = template.Library()

@register.simple_tag
def get_doc(d, tipo, ano, mes):
    return d.get(tipo, {}).get(ano, {}).get(mes, {})

@register.filter
def markdown_html(text):
    html = markdown.markdown(text, extensions=['extra', 'tables', 'nl2br'])
    # Sanitiza o HTML para evitar XSS
    allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS) + ['p', 'pre', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table', 'thead', 'tbody', 'tr', 'th', 'td']
    allowed_attrs = {'*': ['style', 'align']}
    return bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs)

@register.filter
def split(value, delimiter=','):
    """Divide uma string pelo delimitador especificado"""
    if not value:
        return []
    return [item.strip() for item in value.split(delimiter) if item.strip()]

@register.filter
def trim(value):
    """Remove espaços em branco do início e fim da string"""
    if not value:
        return ''
    return value.strip() 