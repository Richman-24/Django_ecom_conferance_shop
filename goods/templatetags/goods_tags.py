from django.utils.http import urlencode
from django import template
from django.db.models import Avg

register = template.Library()

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)


@register.simple_tag()
def average_rating(product):
    rating = product.comments.aggregate(Avg('rating'))['rating__avg']
    if rating:
        return round(rating, 1)
    return "Нет оценок"

@register.simple_tag()
def comments_count(product):
    count = product.comments.count()
    return count