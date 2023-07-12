from .models import Garcom
from django import forms
from pratos.models import Prato
from pedidos.models import PedidoPrato
from django.contrib.auth.hashers import make_password

class PedidoPratoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        prato_id = kwargs.pop("prato_id")
        super().__init__(*args, **kwargs)

        self.fields["adicional"] = forms.ModelMultipleChoiceField(
            queryset=Prato.objects.get(pk=prato_id).adicional,
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.Input):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field_name
                
        self.fields.widget["observacao"].attrs = 'Ex: tirar a cebola, maionese à parte etc.'

        if prato_id:
            self.fields["prato"].initial = prato_id
        self.fields["prato"].widget = forms.HiddenInput()

    class Meta:
        model = PedidoPrato
        fields = ["quantidade", "prato", "adicional", "observacao"]
        widgets = {
            "quantidade": forms.NumberInput(attrs={"min": 1}),
        }


class PedidoPratoGarcomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        prato_id = kwargs.pop("prato_id")
        super().__init__(*args, **kwargs)

        self.fields["adicional"] = forms.ModelMultipleChoiceField(
            queryset=Prato.objects.get(pk=prato_id).adicional,
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.Input):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field_name
                
        self.fields.widget["observacao"].attrs = 'Ex: tirar a cebola, maionese à parte etc.'

        if prato_id:
            self.fields["prato"].initial = prato_id
        self.fields["prato"].widget = forms.HiddenInput()

    class Meta:
        model = PedidoPrato
        fields = ["nome_cliente", "quantidade", "prato", "adicional", "observacao"]
        widgets = {
            "quantidade": forms.NumberInput(attrs={"min": 1}),
        }
        

class GarcomForm(forms.ModelForm):
    class Meta:
        model = Garcom
        fields = ['username', 'email', 'telefone', 'cpf', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.Input):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field_name
                

    def clean_password(self):
        data = self.cleaned_data["password"]
        
        return make_password(data)
    