from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    
    class Meta:
        model = Evento
        fields = ['nome', 'data_inicio', 'data_termino', 'descricao', 'foto']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type':'date', 'placeholder': 'Date de início', 'class':'form-control'}), 
            'data_termino': forms.DateInput(attrs={'type':'date', 'class':'form-control', 'placeholder': 'Date de término'}),
            'foto': forms.FileInput(attrs={'id':'upload', 'accept':"image/*", 'required':True, 'class':'form-control', 'placeholder':'Foto'}),
            'descricao': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descrição do evento'}),
            'nome': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nome do evento'}),
        }
