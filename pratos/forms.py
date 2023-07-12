from django import forms
from .models import Adicional, Prato, Ingrediente, Receita, IngredienteReceita

class PratoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.Input):
                field.widget.attrs['class'] = 'form-control'

    adicional = forms.ModelMultipleChoiceField(
        queryset=Adicional.objects.all(),
        widget=forms.MultipleChoiceField(attrs={'class': 'form-control'}),
        required=False,
    )

    receita = forms.ModelChoiceField(
        queryset=Receita.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Prato
        fields = ["nome", "disponivel", "categoria", "preco", "foto", "adicional", "receita", "descricao"]



class IngredienteReceitaForm(forms.ModelForm):
    class Meta:
        model = IngredienteReceita
        fields = ['ingrediente', 'quantidade']


class AdicionalForm(forms.ModelForm):
    
    class Meta:
        model = Adicional
        fields = ['nome', 'descricao', 'preco', 'foto']
        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'preco': 'Preço',
            'foto': 'Imagem do Prato'
        }
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'foto': forms.FileInput()
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.Input):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field_name


class IngredienteForm(forms.ModelForm):
    UNIDADES_DE_MEDIDA = [
        ('g', 'Grama'),
        ('kg', 'Quilograma'),
        ('ml', 'Mililitro'),
        ('l', 'Litro'),
        ('cc', 'Colher de Chá'),
        ('cs', 'Colher de Sopa'),
        ('xíc', 'Xícara'),
    ]

    unidade_medida = forms.ChoiceField(choices=UNIDADES_DE_MEDIDA, widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Ingrediente
        fields = ['nome', 'quantidade_estoque', 'categoria', 'unidade_medida']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'quantidade_estoque': forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Estoque'}),
            'categoria': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Categoria'}),
        }
        labels = {
            'nome': 'Nome',
            'quantidade_estoque': 'Estoque',
            'categoria': 'Categoria',
            'unidade_medida': 'Unidade de Medida'
        }
    