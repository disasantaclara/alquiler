from django import template

register = template.Library()

MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']

@register.filter
def fecha_corta(value):
    try:
        return value.strftime(f"%d-{MESES[value.month-1]}-%Y")
    except Exception:
        return value