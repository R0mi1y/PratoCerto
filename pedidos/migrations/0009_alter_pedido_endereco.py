# Generated by Django 4.2.2 on 2023-06-28 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0008_alter_endereco_padrao'),
        ('pedidos', '0008_alter_pedido_endereco_alter_pedidoprato_pedido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='endereco',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='clientes.endereco'),
        ),
    ]