from django import forms
from .models import Adicional, Prato, Ingrediente, Receita, IngredienteReceita

class PratoForm(forms.ModelForm):
    adicional = forms.ModelMultipleChoiceField(
        queryset=Adicional.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    receita = forms.ModelChoiceField(
        queryset=Receita.objects.all(),
        required=False
    )

    class Meta:
        model = Prato
        fields = ["nome", "disponivel", "categoria", "preco", "foto", "adicional", "receita","descricao"]


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

class IngredienteForm(forms.ModelForm):
    
    class Meta:
        model = Ingrediente
        fields = ['nome', 'quantidade_estoque', 'categoria', 'unidade_medida']
        labels = {
            'nome': 'Nome',
            'quantidade_estoque': 'Quantidade em Estoque',
            'categoria': 'Categoria',
            'unidade_medida': 'Unidade de Medida',
        }
