from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=20)
    endereco = models.TextField()
    foto = models.ImageField(default=None, null=True, upload_to="media/")
    cliente_id = models.AutoField(primary_key=True)
    codigo_afiliado = models.CharField(max_length=255, null=False)
    pontos = models.IntegerField("Pontos de afiliado", default=0)
    tipo_conta = models.CharField(max_length=20, default="Cliente")
    
    def __str__(self):
        return self.user.username
    
