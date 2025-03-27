from django import forms
from .models import PointSetting, BusinessHours, Category

class PointSettingForm(forms.ModelForm):
    class Meta:
        model = PointSetting
        fields = ["indication", "indicated", "per_purchase_value", "per_rs", "rs_value"]
        labels = {
            "indication": "Pontos por indicação",
            "indicated": "Pontos para indicado",
            "per_purchase_value": "Pontos por valor da compra",
            "per_rs": "Pontos por R$ gasto",
            "rs_value": "Valor em R$ por ponto",
        }

class BusinessHoursForm(forms.ModelForm):
    class Meta:
        model = BusinessHours
        fields = ["opening_time", "closing_time", "reservation_deadline", "time_jump", "delivery_fee"]
        labels = {
            "opening_time": "Horário de abertura",
            "closing_time": "Horário de encerramento",
            "reservation_deadline": "Dias limite para reserva",
            "time_jump": "Intervalo entre horários",
            "delivery_fee": "Taxa de entrega",
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["label", "image"]
        labels = {
            "label": "Nome da Categoria",
            "image": "Imagem",
        }
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.key = instance.label.lower().replace(" ", "_")
        
        if commit:
            instance.save()
        return instance