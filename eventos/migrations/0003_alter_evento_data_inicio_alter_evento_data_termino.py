# Generated by Django 4.2 on 2023-07-03 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0002_rename_data_evento_data_inicio_evento_data_termino'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='data_inicio',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='evento',
            name='data_termino',
            field=models.DateField(default=None, null=True),
        ),
    ]
