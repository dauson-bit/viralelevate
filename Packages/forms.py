from django import forms
from .models import  Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'link', 'quantity']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter the link to boost'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity', 'min': '1'}),
        }
