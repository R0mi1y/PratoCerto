from django.db import models
from pratos.models import Prato, Adicional
from clientes.models import Cliente
from datetime import datetime

class Mesa(models.Model):
    numero = models.IntegerField("Num_mesa", unique=True)
    status = models.CharField("Status_mesa" ,max_length=20)
    
    def __str__(self):
        return f"Mesa {self.numero}"

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mesa = models.OneToOneField(Mesa, on_delete=models.CASCADE, null=True)
    data_pedido = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=50, default="Pendente")
    total = models.DecimalField("Preco_total", max_digits=10, decimal_places=2)
    taxa_entrega = models.DecimalField("Taxa de Entrega", max_digits=10, decimal_places=2, default=0)
    desconto = models.DecimalField("Desconto", max_digits=10, decimal_places=2, default=0)
    local_retirada = models.CharField("Local de Retirada", max_length=20, choices=[
        ('restaurante', 'Retirar no Restaurante'),
        ('reserva', 'Fazer Reserva'),
        ('entrega', 'Entrega em Casa')
    ])
    metodo_pagamento = models.CharField("Método de Pagamento", max_length=20, choices=[
        ('dinheiro', 'Dinheiro'),
        ('cartao', 'Cartão de Crédito'),
        ('transferencia', 'Transferência Bancária')
    ])
    
    
class PedidoPrato(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='pedidos_pratos')
    prato = models.ForeignKey(Prato, on_delete=models.CASCADE)
    observacao = models.TextField("Observações", blank=True)
    quantidade = models.IntegerField("Quantidade", default=1)
    adicional = models.ManyToManyField(Adicional, blank=True)

    def __str__(self):
        return f"{self.pedido} - {self.prato}"