from django.utils.http import urlencode
from django import template
from django.db.models import Avg

register = template.Library()

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
