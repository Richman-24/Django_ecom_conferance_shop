from django import template

from carts.models import Cart

register = template.Library()

@register.simple_tag()
def user_cart(request):
    if request.user.is_authenticated:
        # return Cart.objects.filter(user=request.user)
        queryset = Cart.objects.filter(user=request.user)
        data = {}
        data['carts'] = queryset
        data['product_list'] = queryset.values_list('product', flat=True)
        return data

@register.filter
def get_item(cart_list, product_id):
    for cart in cart_list:
        if cart.product.id == product_id:
            return cart
    return None