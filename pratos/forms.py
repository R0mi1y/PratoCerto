from django import forms

from PratoCerto.settings import CACHED_CATEGORIES
from settings.models import Category
from .models import Adicional, Prato, Ingrediente, Receita, IngredienteReceita
from django.db.utils import OperationalError, ProgrammingError

try:
    CATEGORY_CHOICES = [(category.key, category.label) for category in Category.objects.all()]
except (OperationalError, ProgrammingError):
    CATEGORY_CHOICES = []


class PratoForm(forms.ModelForm):

    adicional = forms.ModelMultipleChoiceField(
        queryset=Adicional.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
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
        widgets = {
            "categoria": forms.Select(
                attrs={'class': 'form-control'},
                choices=CATEGORY_CHOICES
            ),
            "descricao":forms.Textarea(attrs={'class': 'form-control'}),
            "nome": forms.TextInput(attrs={'class': 'form-control'}),
            "preco": forms.NumberInput(attrs={'class': 'form-control'}),
            "foto": forms.FileInput(attrs={'class': 'form-control'}),
            "disponivel": forms.CheckboxInput(attrs={'class':'form-control-checkbox'}),
        }


class IngredienteReceitaForm(forms.ModelForm):
    class Meta:
        model = IngredienteReceita
        fields = ['ingrediente', 'quantidade']


class AdicionalForm(forms.ModelForm):
    
    class Meta:
        model = Adicional
        fields = ['nome', 'descricao', 'preco', 'foto']
        widgets = {
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Preço'}),
            'nome': forms.TextInput(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Nome'}),
            'descricao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Descrição'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'})
        }


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
    