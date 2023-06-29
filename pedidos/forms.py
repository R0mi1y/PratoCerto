from datetime import datetime, timedelta
from django import forms
from clientes.models import Endereco, Cliente
from PratoCerto.settings import AUX
from pratos.models import Prato
from .models import Pedido, PedidoPrato, Reserva, Mesa


class PedidoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            cliente = Cliente.objects.get(cliente_id=kwargs.pop("cliente_id"))
            super().__init__(*args, **kwargs)

            self.fields["endereco"] = forms.ModelMultipleChoiceField(
                queryset=Endereco.objects.filter(cliente=cliente),
            )
        except:
            pass


    class Meta:
        model = Pedido
        fields = ["local_retirada", 'metodo_pagamento', "endereco"]


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
            "quantidade": forms.NumberInput(attrs={"min": 1}),
            "observacao": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Ex: tirar a cebola, maionese à parte etc.",
                }
            ),
        }

class ReservaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        cliente_id = kwargs.pop("cliente_id")
        super().__init__(*args, **kwargs)

        if cliente_id:
            self.fields["cliente"].initial = cliente_id

        self.fields["cliente"].widget = forms.HiddenInput()
        self.fields["preco_total"].widget = forms.HiddenInput()
        
        self.fields["mesa"] = forms.ModelMultipleChoiceField(
            queryset=Mesa.objects.filter(status="disponível"),
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )

        # Choices de horário
        if AUX["horario_pulo"] != 24:
            hora_inicio = datetime.strptime(AUX["horario_abertura"], "%H:%M")
            hora_fim = datetime.strptime(AUX["horario_encerramento"], "%H:%M")
            delta = timedelta(hours=AUX["horario_pulo"])
            horarios_choices = []
            hora_atual = hora_inicio
            while hora_atual <= hora_fim:
                horarios_choices.append(
                    (hora_atual.strftime("%H:%M"), hora_atual.strftime("%H:%M"))
                )
                hora_atual += delta
            self.fields["horario"] = forms.ChoiceField(choices=horarios_choices)
        else:
            self.fields["horario"].widget = forms.HiddenInput(attrs={'required': False, 'value':"00:00"})
            self.fields["horario"].label = ''
        # Choices de data
        data_inicio = datetime.now().date()
        data_fim = data_inicio + timedelta(days=(AUX["data_limite_reserva"]-1))
        datas_choices = []
        data_atual = data_inicio
        while data_atual <= data_fim:
            datas_choices.append((data_atual, data_atual.strftime("%d/%m/%Y")))
            data_atual += timedelta(days=1)
        self.fields["data_reserva"] = forms.ChoiceField(choices=datas_choices)

    class Meta:
        model = Reserva
        fields = [
            "cliente",
            "mesa",
            "data_reserva",
            "horario",
            "qnt_pessoas",
            "preco_total",
            "observacao",
        ]
        widgets = {
            "observacao": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Ex: Festa de aniversário, reuniões de negócios, comemorações familiares, etc.",
                }
            ),
        }
        
    def clean_horario(self):
        data = self.cleaned_data["horario"]
        if data == '':
            return None
        return data

    