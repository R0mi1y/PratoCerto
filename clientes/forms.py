from django import forms
from .models import Cliente, Endereco
from PratoCerto.settings import AUX
from django.contrib.auth.hashers import make_password


class ClienteForm(forms.ModelForm):
    indicador = forms.CharField(max_length=20, required=False, widget=forms.TextInput(
<<<<<<< HEAD
        attrs={'class': 'form-control', 'placeholder': 'Código de Indicação (Opcional)'}
=======
        attrs={'class': 'form-control', 'placeholder': 'Código de quem te indicou'}
>>>>>>> ccad9915a5966fbe37a5a6e79b8b4814d46c5cc8
    ))
    pontos = forms.CharField(
        max_length=20, required=False, widget=forms.HiddenInput(attrs={"class": ""}),
        label="",
    )

    class Meta:
        model = Cliente
        fields = ["telefone", "cpf", "pontos", "email", "username", "password"]

        widgets = {
            "password": forms.PasswordInput(
                attrs={"autocomplete": "new-password", "class": "form-control", "placeholder":"Senha"}
            ),
            "email": forms.EmailInput(
                attrs={"autocomplete": "new-email", "class": "form-control", "placeholder":"Email"}
            ),
            "telefone" : forms.TextInput(
                attrs={"class": "form-control", "placeholder":"Telefone"}
            ),
            "cpf" : forms.TextInput(
                attrs={"class": "form-control", "placeholder":"CPF"}
            ),
            "username" : forms.TextInput(
                attrs={"class": "form-control", "placeholder":"Seu Nome"}
            )
        }
        
    def clean_password(self):
        data = self.cleaned_data["password"]
        
        return make_password(data)
    
        
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
    
    
    
class ClienteFormEditar(forms.ModelForm):
    foto = forms.ImageField(widget=forms.FileInput(attrs={
        "accept": "image/*",
    }), required=False)
    
    class Meta:
        model = Cliente
        fields = ["telefone", "cpf", "email", "foto"]

        widgets = {
            "password": forms.PasswordInput(
                attrs={"autocomplete": "new-password", "class": "custom-class"}
            ),
        }
        
    def clean_password(self):
        data = self.cleaned_data["password"]
        
        return make_password(data)
    
        
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
        
        
        
class ClienteFormAdmin(forms.ModelForm):
    telefone = forms.CharField(required=False)
    foto = forms.ImageField(required=False)
    cpf = forms.CharField(required=False)

    class Meta:
        model = Cliente
        fields = ["telefone", "foto", "cpf", "email", "username"]

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
