# Generated by Django 4.2 on 2023-07-06 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0003_alter_evento_data_inicio_alter_evento_data_termino'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='foto',
            field=models.ImageField(default='None', upload_to='media/'),
            preserve_default=False,
        ),
    ]
