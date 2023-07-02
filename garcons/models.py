from django.db import models
from django.contrib.auth.models import AbstractUser
from clientes.models import Cliente

# Create your models here.
class Garcom(Cliente):
    observacoes = models.TextField()
    
    def __str__(self):
        return self.username