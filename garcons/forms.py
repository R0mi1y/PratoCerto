from django import forms
from pratos.models import Prato
from pedidos.models import PedidoPrato, Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['mesa']


class PedidoPratoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        prato_id = kwargs.pop("prato_id")
        super().__init__(*args, **kwargs)

        self.fields["adicional"] = forms.ModelMultipleChoiceField(
            queryset=Prato.objects.get(pk=prato_id).adicional,
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )

        if prato_id:
            self.fields["prato"].initial = prato_id
        self.fields["prato"].widget = forms.HiddenInput()

    class Meta:
        model = PedidoPrato
        fields = ["quantidade", "prato", "adicional", "observacao"]
        widgets = {
            "observacao": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Ex: tirar a cebola, maionese à parte etc.",
                }
            ),
        }