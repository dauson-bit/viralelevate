from django import forms
from .models import PaymentSupportRequest, Order

class PaymentSupportForm(forms.ModelForm):
    class Meta:
        model = PaymentSupportRequest
        fields = ['name', 'email', 'issue', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name', 'id': 'supportName'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email', 'id': 'supportEmail'}),
            'issue': forms.Select(attrs={'class': 'form-select', 'id': 'supportIssue'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Please describe your issue', 'id': 'supportMessage'}),
        }

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
