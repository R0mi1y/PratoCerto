from django.contrib import messages
from django.shortcuts import redirect, render
from clientes.models import Cliente
from pedidos.models import *
from pedidos.forms import *
from pratos.models import *
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator
from .forms import AdminForm
from PratoCerto.settings import AUX
from main.models import Referencia


# Create your views here.
@has_role_decorator("admin")
def criar_editar_admin(request, id=None):
    admin = None

    if id:
        admin = Cliente.objects.get(tipo_conta="admin", id=id)

    if request.method == "POST":
        form = AdminForm(request.POST, instance=admin)

        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.tipo_conta = "Admin"
            cliente.is_superuser = True
            cliente.save()
            assign_role(cliente, "admin")
            
            return redirect("home_admin")
    else:
        form = AdminForm(instance=admin)

    return render(request, "models/forms/form.html", {"form": form, "titulo":"Criar conta Admin"})


@has_role_decorator("admin")
def remover_carrinho(request, id):
    try:
        PedidoPrato.objects.get(id=id).delete()
    except PedidoPrato.objects.DoesNotExist:
        messages.error("O pedido não existe!")

    return redirect("ver carrinho")


@has_role_decorator("admin")
def home(request):
    return redirect("home_cliente")


@has_role_decorator("admin")
def deletar_recomendacao(request, id):
    Referencia.objects.filter(chave="recomendacoes", valor=str(id)).delete()
    return redirect("gerenciar_recomendacoes")
    
    
@has_role_decorator("admin")
def add_recomendacao(request, id=None):
    if id:
        Referencia.objects.create(chave="recomendacoes", valor=id)
    return redirect("gerenciar_recomendacoes")


@has_role_decorator("admin")
def ver_recomendacoes(request):
    id_pratos = Referencia.objects.filter(chave="recomendacoes")
    
    recomendados = []
    [recomendados.append(int(i.valor)) for i in id_pratos]
    
    print(recomendados)
        
    pratos = Prato.objects.all()
    return render(request, "models/admin_gerente/set_pratos_recomendacoes.html",{"pratos":pratos, "recomendados":recomendados})