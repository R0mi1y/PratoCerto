from django.db import models
from pratos.models import Prato, Adicional
from clientes.models import Cliente, Endereco
from datetime import datetime


class Mesa(models.Model):
    numero = models.IntegerField(
        "Numero da mesa",
        unique=True,
    )
    status = models.CharField(
        "Status da mesa",
        max_length=20,
        default="disponível",
    )

    def __str__(self):
        return f"mesa {self.numero}"


class Pedido(models.Model):
    mesa = models.ForeignKey(
        Mesa,on_delete=models.CASCADE, null=True,
        )
    data_pedido = models.DateTimeField(
        default=datetime.now,
        )
    status = models.CharField(
        max_length=50, default="Pendente",
        )
    total = models.DecimalField(
        "Preco total do pedido", max_digits=10, decimal_places=2, null=True,
        )
    taxa_entrega = models.DecimalField(
        "Taxa de Entrega", max_digits=10, decimal_places=2, default=0,
        )
    desconto = models.DecimalField(
        "Desconto", max_digits=10, decimal_places=2, default=0,
    )
    local_retirada = models.CharField(
        "Local de Retirada", max_length=20,
        choices=[
            ("restaurante", "Retirar no Restaurante"),
            ("entrega", "Entrega em Casa"),
        ], null=True
    )
    metodo_pagamento = models.CharField(
        "Método de Pagamento", max_length=20,
        choices=[
            ("dinheiro", "Dinheiro"),
            ("cartao", "Cartão de Crédito"),
            ("transferencia", "Transferência Bancária"),
        ], null=True,
    )
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True,
    )


class PedidoPrato(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        null=True,
    )
    nome_cliente = models.CharField(max_length=30, null=True)
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name="pedidos_pratos", default=None, null=True
    )
    status = models.CharField(
        max_length=50,
        default="No Carrinho",
    )
    prato = models.ForeignKey(Prato, on_delete=models.CASCADE)
    observacao = models.TextField("Observações", blank=True, default=None)
    quantidade = models.IntegerField("Quantidade", default=1)
    adicional = models.ManyToManyField(Adicional, blank=True)

    def __str__(self):
        return f"{self.pedido} - {self.prato}"


class Reserva(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
    )
    mesa = models.ManyToManyField(
        Mesa,
    )
    data_reserva = models.DateField()
    horario = models.TimeField(null=True)
    observacao = models.TextField("Observações", blank=True, default=None)
    qnt_pessoas = models.IntegerField(default="1")
    preco_total = models.DecimalField(
        "Preco total da resarva",
        max_digits=10,
        decimal_places=2,
        null=True,
    )
    status = models.CharField("status", max_length=20, default="Pendente")

    def __str__(self):
        return str(self.data_reserva) + str(self.horario) + self.status
