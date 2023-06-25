from django.db import models
from PratoCerto.settings import AUX


class Adicional(models.Model):
    nome = models.CharField("Nome", max_length=40)
    descricao = models.TextField("Descrição")
    preco = models.DecimalField("Preco", max_digits=10, decimal_places=2)
    foto = models.ImageField("Imagem_do_prato", default=None, null=True, upload_to="pratos/")
    
    def __str__(self):
        return self.nome


class Prato(models.Model):
    nome = models.CharField("Nome", max_length=40)
    disponivel = models.BooleanField("Disponível", default=False)
    categoria = models.CharField("Categoria", max_length=30, choices=AUX["Categorias"])
    foto = models.ImageField("Imagem_do_prato", default=None, null=True, upload_to="pratos/")
    preco = models.DecimalField("Preco", max_digits=7, decimal_places=2)
    descricao = models.TextField("Descrição")
    adicional = models.ManyToManyField(Adicional, "adicionais")
    
    def __str__(self):
        return self.nome