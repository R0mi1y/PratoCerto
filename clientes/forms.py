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
    indicador = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Cliente
        fields = ["telefone", "cpf", "endereco"]
        
    def clean_indicador(self):
        indicador = self.cleaned_data.get("indicador")
        
        if indicador and indicador != '':
            try:
                Cliente.objects.get(codigo_afiliado=indicador)
            except Cliente.DoesNotExist:
                raise forms.ValidationError("Código do indicador inválido.")

        return indicador
