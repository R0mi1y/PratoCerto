# Generated by Django 4.2.2 on 2023-06-27 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0004_cliente_pontos'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='tipo_conta',
            field=models.CharField(default='Cliente', max_length=20),
        ),
    ]