from django import forms
from clientes.models import Cliente
from django.contrib.auth.hashers import make_password

class AdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Cliente
        fields = ['username', 'password', 'email']
        
    def clean_password(self):
        data = self.cleaned_data["password"]
        
        return make_password(data)