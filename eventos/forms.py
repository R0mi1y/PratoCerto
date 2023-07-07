from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    
    class Meta:
        model = Evento
        fields = ['nome', 'data_inicio', 'data_termino', 'descricao', 'foto']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type':'date'}), 
            'data_termino': forms.DateInput(attrs={'type':'date'}),
            'foto': forms.FileInput(attrs={'id':'upload', 'accept':"image/*", 'required':True})
        }