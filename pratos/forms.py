from django import forms
from .models import Adicional, Prato

class PratoForm(forms.ModelForm):
    adicional = forms.ModelMultipleChoiceField(
        queryset=Adicional.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Prato
        fields = ["nome", "disponivel", "categoria", "preco", "foto", "adicional", "descricao"]


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
        }
