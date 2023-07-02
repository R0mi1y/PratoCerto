from django.db import models
from clientes.models import Cliente

class Caixa(Cliente):
    observacoes = models.TextField()
    
    def __str__(self):
        return self.username