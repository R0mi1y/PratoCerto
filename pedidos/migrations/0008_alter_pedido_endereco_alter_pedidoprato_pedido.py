# Generated by Django 4.2.2 on 2023-06-27 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0007_pedidoprato_cliente_pedidoprato_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='endereco',
            field=models.TextField(verbose_name='Endereço'),
        ),
        migrations.AlterField(
            model_name='pedidoprato',
            name='pedido',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pedidos_pratos', to='pedidos.pedido'),
        ),
    ]