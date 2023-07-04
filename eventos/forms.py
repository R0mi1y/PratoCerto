from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nome', 'data_inicio', 'data_termino', 'descricao']
        widgets = {
            'data_inicio': forms.DateInput(), 
            'data_termino': forms.DateInput(),
        }
