from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
    
    
class Cliente(AbstractUser):
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=20, null=True)
    foto = models.ImageField(default=None, null=True, upload_to="media/")
    cliente_id = models.AutoField(primary_key=True)
    codigo_afiliado = models.CharField(max_length=255, null=False)
    pontos = models.IntegerField("Pontos de afiliado", default=0)
    tipo_conta = models.CharField(max_length=20, default="Cliente")
    
    def __str__(self):
        return self.username
    

class Endereco(models.Model):
    nome = models.CharField(max_length=40)
    telefone = models.CharField(max_length=20)
    cep = models.CharField(max_length=8)
    pais = models.CharField(max_length=100, default='Brasil')
    estado_cidade = models.CharField(max_length=200)
    bairro = models.CharField(max_length=100)
    rua = models.CharField(max_length=100)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=100, blank=True, null=True)
    padrao = models.BooleanField(default=False)
    cliente = models.ForeignKey(Cliente, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.rua}, {self.estado_cidade} - CEP: {self.cep}"
    
    
@receiver(pre_save, sender=Endereco)
def set_default_endereco(sender, instance, **kwargs):
    if instance.padrao:
        # Set all other addresses of the same client as not default
        Endereco.objects.filter(cliente=instance.cliente).exclude(pk=instance.pk).update(padrao=False)


@receiver(post_save, sender=Endereco)
def check_default_endereco(sender, instance, **kwargs):
    if not instance.padrao:
        # Check if there are no default addresses for the same client, set the first one as default
        default_endereco = Endereco.objects.filter(cliente=instance.cliente, padrao=True).first()
        if not default_endereco:
            instance.padrao = True
            instance.save()