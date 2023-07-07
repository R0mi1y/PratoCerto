from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from clientes.models import Cliente
from clientes.forms import ClienteFormAdmin
from pratos.models import Prato
from pratos.forms import PratoForm, AdicionalForm
from cozinhas.forms import CozinhaForm
from cozinhas.models import Cozinha
from garcons.forms import GarcomForm
from garcons.models import Garcom
from caixas.forms import CaixaForm
from caixas.models import Caixa
from pedidos.models import *
from pedidos.forms import *
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator
from .forms import AdminForm
from clientes.views import gerar_aleatorio


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




