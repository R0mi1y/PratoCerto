from django import forms
from .models import User, Cliente


class UserClienteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "username", "password"]
        widgets = {
            "password": forms.PasswordInput(
                attrs={"autocomplete": "new-password", "class": "custom-class"}
            ),
        }
    
    # def 


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ["telefone", "cpf", "endereco"]
