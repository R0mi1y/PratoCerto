# Generated by Django 4.2 on 2023-07-07 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pratos', '0004_ingrediente_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingrediente',
            name='unidade',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
    ]
