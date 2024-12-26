from django.utils.http import urlencode
from django import template
from django.db.models import Avg

from goods.models import Product

register = template.Library()

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
