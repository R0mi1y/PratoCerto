# Generated by Django 4.2 on 2023-07-03 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evento',
            old_name='data',
            new_name='data_inicio',
        ),
        migrations.AddField(
            model_name='evento',
            name='data_termino',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
    ]
