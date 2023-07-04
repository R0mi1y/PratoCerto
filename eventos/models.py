from django.db import models

# Create your models here.
from django.db import models

class Evento(models.Model):
    nome = models.CharField(max_length=100)
    data_inicio = models.DateField(null=True, default=None)
    data_termino = models.DateField(null=True, default=None)
    descricao = models.TextField()
    def __str__(self):
        return self.nome
