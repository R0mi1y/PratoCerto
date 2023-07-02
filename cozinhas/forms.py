from django import forms
from .models import Cozinha
from django.contrib.auth.hashers import make_password


class CozinhaForm(forms.ModelForm):
    class Meta:
        model = Cozinha
        fields = ['username', 'email', 'telefone', 'cpf', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_password(self):
        data = self.cleaned_data["password"]
        
        return make_password(data)