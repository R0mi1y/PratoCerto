from django import forms
from .models import Cozinha
from django.contrib.auth.hashers import make_password


class CozinhaForm(forms.ModelForm):
    class Meta:
        model = Cozinha
        fields = ['username', 'email', 'telefone', 'cpf', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'cpf'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'telefone'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_password(self):
        data = self.cleaned_data["password"]
        
        return make_password(data)