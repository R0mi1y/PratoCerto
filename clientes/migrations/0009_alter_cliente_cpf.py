# Generated by Django 4.2.2 on 2023-06-29 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0008_alter_endereco_padrao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cpf',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]