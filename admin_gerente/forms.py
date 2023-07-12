from django import forms
from clientes.models import Cliente
from pratos.models import Prato
from django.contrib.auth.hashers import make_password

class AdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), help_text=None)

    class Meta:
        model = Cliente
        fields = ['username', 'password', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }