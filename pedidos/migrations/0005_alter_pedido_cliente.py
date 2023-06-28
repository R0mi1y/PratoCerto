# Generated by Django 4.2.2 on 2023-06-27 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0005_cliente_tipo_conta'),
        ('pedidos', '0004_alter_pedido_local_retirada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente'),
        ),
    ]
