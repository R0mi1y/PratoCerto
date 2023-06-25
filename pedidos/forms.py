from django import forms
from pratos.models import Prato
from .models import Pedido, PedidoPrato

class PedidoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        cliente_id = kwargs.pop('cliente_id')  # Obtém o ID do prato passado como argumento
        super().__init__(*args, **kwargs)
        if cliente_id:
            self.fields['cliente'].initial = cliente_id  # Define o valor inicial do campo "cliente"
        self.fields['cliente'].widget = forms.HiddenInput()  # Torna o campo "cliente" invisível
    
    class Meta:
        model = Pedido
        fields = ['cliente', 'local_retirada']
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 3}),
        }
        

class PedidoPratoForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        prato_id = kwargs.pop('prato_id')
        super().__init__(*args, **kwargs)
        
        self.fields['adicional'] = forms.ModelMultipleChoiceField(
            queryset=Prato.objects.get(pk=prato_id).adicional,
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        
        if prato_id:
            self.fields['prato'].initial = prato_id
        self.fields['prato'].widget = forms.HiddenInput()
    
    class Meta:
        model = PedidoPrato
        fields = ['quantidade', 'prato', 'adicional', 'observacao']
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 3, 'placeholder':"Ex: tirar a cebola, maionese à parte etc."}),
        }

