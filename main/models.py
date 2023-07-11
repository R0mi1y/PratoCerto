from django.db import models

# Create your models here.
class Referencia(models.Model):
    chave = models.CharField(max_length=50)
    valor = models.TextField()