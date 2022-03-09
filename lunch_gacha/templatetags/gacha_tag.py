from django import template


register = template.Library()


@register.filter
def list_all(value):
    """m2mの内容を表示する

    """
    if value.count():
        return ', '.join([str(x) for x in value.all()])
    else:
        return '(なし)'
