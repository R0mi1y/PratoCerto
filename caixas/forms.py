from django import forms
from .models import Caixa
from django.contrib.auth.hashers import make_password


class CaixaForm(forms.ModelForm):
    class Meta:
        model = Caixa
        fields = ['username', 'email', 'telefone', 'cpf', 'password']
        widgets = {
            'password':forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_password(self):
        data = self.cleaned_data["password"]
        
        return make_password(data)