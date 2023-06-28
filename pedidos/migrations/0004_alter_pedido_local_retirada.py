# Generated by Django 4.2.2 on 2023-06-27 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0003_remove_reserva_pedido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='local_retirada',
            field=models.CharField(choices=[('restaurante', 'Retirar no Restaurante'), ('entrega', 'Entrega em Casa')], max_length=20, verbose_name='Local de Retirada'),
        ),
    ]