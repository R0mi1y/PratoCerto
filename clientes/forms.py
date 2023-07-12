from django import forms
from .models import Cliente, Endereco
from PratoCerto.settings import AUX
from django.contrib.auth.hashers import make_password


class ClienteForm(forms.ModelForm):
    indicador = forms.CharField(max_length=20, required=False, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Código de Indicação (Opcional)'}
        )
    )
    pontos = forms.CharField(required=False, widget=forms.HiddenInput())

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
    
    
    
class ClienteFormEditar(forms.ModelForm):
    foto = forms.ImageField(widget=forms.FileInput(attrs={
        "accept": "image/*",
        'class': "form-control",
    }), required=False)
    
    class Meta:
        model = Cliente
        fields = ["telefone", "cpf", "email", "foto"]
        widgets = {
            "email": forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder':'Email'}
            ),
            "telefone" : forms.TextInput(
                attrs={"class": "form-control", "placeholder":"Telefone"}
            ),
            "cpf" : forms.TextInput(
                attrs={"class": "form-control", "placeholder":"CPF"}
            ),
            "foto" : forms.FileInput(
                attrs={"class": "form-control", "placeholder":"Foto"}
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
        
        
        
class ClienteFormAdmin(forms.ModelForm):
    telefone = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Telefone'}
    ))
    foto = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'form-control', 'placeholder': 'Foto'}
    ))
    cpf = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'CPF'}
    ))

    class Meta:
        model = Cliente
        fields = ["telefone", "foto", "cpf", "email", "username"]

    def clean_username(self):
        data = self.cleaned_data["username"]

        return data


class EnderecoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.Input):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field_name
                
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.Input):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field_name
                
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
