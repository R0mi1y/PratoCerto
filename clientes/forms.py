from django import forms
from .models import User, Cliente, Endereco
from PratoCerto.settings import AUX


class ClienteForm(forms.ModelForm):
    indicador = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Cliente
        fields = ["telefone", "cpf", "pontos", "email", "username", "password"]

        widgets = {
            "pontos": forms.HiddenInput(),
            "password": forms.PasswordInput(
                attrs={"autocomplete": "new-password", "class": "custom-class"}
            ),
        }

    def clean_indicador(self):
        indicador = self.cleaned_data.get("indicador")

        if indicador and indicador != "":
            try:
                Cliente.objects.get(codigo_afiliado=indicador).pontos += AUX["pontos"][
                    "indicação"
                ]
                self.cleaned_data["pontos"] += AUX["pontos"]["indicado"]
            except Cliente.DoesNotExist:
                raise forms.ValidationError("Código do indicador inválido.")

        return indicador
    
    def clean_username(self):
        data = self.cleaned_data["username"]
        
        return data
    


class EnderecoForm(forms.ModelForm):
    padrao = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    
    class Meta:
        model = Endereco
        fields = [
            "nome",
            "telefone",
            "cep",
            "pais",
            "estado_cidade",
            "bairro",
            "rua",
            "numero",
            "complemento",
            "padrao",
        ]
        
        
class EditarEnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = [
            "nome",
            "telefone",
            "cep",
            "pais",
            "estado_cidade",
            "bairro",
            "rua",
            "numero",
            "complemento",
        ]
