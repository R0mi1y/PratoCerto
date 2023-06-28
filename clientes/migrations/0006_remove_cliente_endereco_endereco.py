# Generated by Django 4.2.2 on 2023-06-28 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0005_cliente_tipo_conta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='endereco',
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.CharField(max_length=8)),
                ('rua', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=100)),
                ('numero', models.IntegerField()),
                ('complemento', models.CharField(blank=True, max_length=100, null=True)),
                ('bairro', models.CharField(max_length=100)),
                ('pais', models.CharField(default='Brasil', max_length=100)),
                ('ponto_referencia', models.CharField(blank=True, max_length=200, null=True)),
                ('cliente', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente')),
            ],
        ),
    ]
