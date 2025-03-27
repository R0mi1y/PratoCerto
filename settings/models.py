import json
from django.db import models
from django.db import models

class Category(models.Model):
    key = models.CharField(max_length=50, unique=True)  # Valor salvo no BD
    label = models.CharField(max_length=50)  # Nome visível para o usuário
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    
    def __str__(self):
        return self.label

class PointSetting(models.Model):
    indication = models.PositiveIntegerField(default=20)  # Pontos para indicação
    indicated = models.PositiveIntegerField(default=10)  # Pontos para indicado
    per_purchase_value = models.PositiveIntegerField(default=10)  # Pontos por compra
    per_rs = models.PositiveIntegerField(default=1)  # Pontos por real gasto
    rs_value = models.FloatField(default=0.2)  # Valor em reais por ponto

    def __str__(self):
        return "Configurações de Pontos"

class BusinessHours(models.Model):
    opening_time = models.TimeField(default='09:00')  # Horário de abertura
    closing_time = models.TimeField(default='21:00')  # Horário de encerramento
    reservation_deadline = models.PositiveIntegerField(default=9)  # Data limite de reserva
    time_jump = models.PositiveIntegerField(default=1)  # Intervalo entre horários (24 para desativar)
    delivery_fee = models.FloatField(default=8.0)  # Valor do frete

    def __str__(self):
        return f"{self.opening_time} - {self.closing_time}"

def get_combined_json():
    categories = Category.objects.all().values('key', 'label', 'image')
    
    # Definir valores padrão para evitar erro se não houver registros
    default_points = {
        "indicação": 0,
        "indicado": 0,
        "por_valor_compra": 0,
        "por_rs": 0,
        "valor_rs": 0.0,
    }

    default_hours = {
        "horario_abertura": "00:00",
        "horario_encerramento": "23:59",
        "data_limite_reserva": 0,
        "horario_pulo": 0,
        "frete_entrega": 0.0,
    }

    points = PointSetting.objects.first()
    hours = BusinessHours.objects.first()

    data = {
        "Categorias": list(categories),
        "pontos": {
            "indicação": points.indication if points else default_points["indicação"],
            "indicado": points.indicated if points else default_points["indicado"],
            "por_valor_compra": points.per_purchase_value if points else default_points["por_valor_compra"],
            "por_rs": points.per_rs if points else default_points["por_rs"],
            "valor_rs": points.rs_value if points else default_points["valor_rs"],
        },
        "horario_abertura": hours.opening_time.strftime("%H:%M") if hours else default_hours["horario_abertura"],
        "horario_encerramento": hours.closing_time.strftime("%H:%M") if hours else default_hours["horario_encerramento"],
        "data_limite_reserva": hours.reservation_deadline if hours else default_hours["data_limite_reserva"],
        "horario_pulo": hours.time_jump if hours else default_hours["horario_pulo"],
        "frete_entrega": hours.delivery_fee if hours else default_hours["frete_entrega"],
    }

    return json.dumps(data, ensure_ascii=False, indent=4)
