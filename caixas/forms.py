from django import forms
from .models import Caixa
from django.contrib.auth.hashers import make_password


class CaixaForm(forms.ModelForm):
    class Meta:
        model = Caixa
        fields = ['username', 'email', 'telefone', 'cpf', 'password']
        widgets = {
            'password':forms.PasswordInput(attrs={'class': 'form-control'}),
            'username':forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class': 'form-control'}),
            'cpf':forms.TextInput(attrs={'class': 'form-control'}),
            'telefone':forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_password(self):
        data = self.cleaned_data["password"]
        
        return make_password(data)