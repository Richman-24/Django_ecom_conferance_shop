from django import forms

from .models import Order

class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'required_delivery',
            'delivery_adress',
        ]

        widgets = {
            'delivery_adress': forms.TextInput(attrs={'placeholder': 'Введите адрес доставки'}),
        }