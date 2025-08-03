from django.db import models

class Referencia(models.Model):
    chave = models.CharField(max_length=50)
    valor = models.TextField()