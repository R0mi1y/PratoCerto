from django import forms
from .models import User, Cliente, Endereco
from PratoCerto.settings import AUX


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
        fields = ["telefone", "cpf", "pontos"]

        widgets = {
            "pontos": forms.HiddenInput(),
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


class ClienteForm(forms.ModelForm):
    indicador = forms.CharField(max_length=20, required=False)
    pontos = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Cliente
        fields = ["telefone", "cpf", "pontos"]

    def clean_indicador(self):
        indicador = self.cleaned_data.get("indicador")

        if indicador and indicador != "":
            try:
                cliente_indicador = Cliente.objects.get(codigo_afiliado=indicador)
                self.cleaned_data["pontos"] = AUX["pontos"]["indicado"]
                cliente_indicador.pontos += AUX["pontos"]["indicação"]
                cliente_indicador.save()
            except Cliente.DoesNotExist:
                raise forms.ValidationError("Código do indicador inválido.")

        return indicador


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
