# Generated by Django 4.2.2 on 2023-06-25 17:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('telefone', models.CharField(max_length=20)),
                ('cpf', models.CharField(max_length=20)),
                ('endereco', models.TextField()),
                ('foto', models.ImageField(default=None, null=True, upload_to='media/')),
                ('cliente_id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
