# Generated by Django 4.2.2 on 2023-07-11 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pratos', '0011_receita_nome'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prato',
            name='ingredientes',
        ),
        migrations.AlterField(
            model_name='adicional',
            name='foto',
            field=models.ImageField(default=None, null=True, upload_to='pratos/%Y/%m/%d/', verbose_name='Imagem_do_prato'),
        ),
    ]
