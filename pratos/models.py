from django.db import models
from clientes.models import Cliente
from PratoCerto.settings import AUX


class Adicional(models.Model):
    nome = models.CharField("Nome", max_length=40)
    descricao = models.TextField("Descrição")
    preco = models.DecimalField("Preco", max_digits=10, decimal_places=2)
    foto = models.ImageField("Imagem_do_prato", default=None, null=True, upload_to="pratos/")
    
    def __str__(self):
        return self.nome + " R$ " + str(self.preco)
    
    
class Comentario(models.Model):
    texto = models.TextField("comentário")
    respostas = models.ManyToManyField('self', blank=True, symmetrical=False)
    likes = models.IntegerField("likes", default=0)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
    

class Ingrediente(models.Model):
    nome = models.CharField("Nome", max_length=40)
    quantidade_estoque = models.PositiveIntegerField("Quantidade_Estoque")
    categoria = models.CharField("Categoria", max_length= 50 )
    unidade_medida = models.CharField(max_length=50)
    
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
    comentarios = models.ManyToManyField(Comentario, "comentarios", default=None)
    ingredientes = models.ManyToManyField(Ingrediente, "ingredientes")

    def __str__(self):
        return self.nome
    


class Receita(models.Model):
    nome = models.CharField(max_length=50)
    prato = models.OneToOneField('Prato', on_delete=models.CASCADE, null=True)
    ingredientes_disponiveis = models.BooleanField('ingredientes_disponiveis', default=False)
    def __str__(self):
        return f"Receita do {self.nome}"


class IngredienteReceita(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.receita} - {self.ingrediente}: {self.quantidade} {self.ingrediente.unidade_medida}"