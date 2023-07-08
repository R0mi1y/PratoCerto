from django.contrib import messages
from django.shortcuts import redirect, render
from clientes.models import Cliente
from pedidos.models import *
from pedidos.forms import *
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator
from .forms import AdminForm
from PratoCerto.settings import AUX


# Create your views here.
@has_role_decorator("admin")
def criar_editar_admin(request, id=None):
    admin = None

    if id:
        admin = Cliente.objects.get(tipo_conta="admin", id=id)

    if request.method == "POST":
        form = AdminForm(request.POST)

        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.tipo_conta = "Admin"
            cliente.is_superuser = True
            cliente.save()
            assign_role(cliente, "admin")
            
            return redirect("home_admin")
    else:
        form = AdminForm(instance=admin)

    return render(request, "models/forms/form.html", {"form": form})


@has_role_decorator("admin")
def remover_carrinho(request, id):
    try:
        PedidoPrato.objects.get(id=id).delete()
    except PedidoPrato.objects.DoesNotExist:
        messages.error("O pedido não existe!")

    return redirect("ver carrinho")


def home(request):
    return redirect("home_cliente")


def ver_recomendacoes(request):
    
    
    return redirect("models/admin_gerente/gerencia_recomendacoes.html")


def deletar_recomendacao(request):
    pass


def add_recomendacao(request):
    pass