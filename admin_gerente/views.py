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


# Create your views here.
@has_role_decorator("admin")
def criar_editar_admin(request, id):
    admin = None

    if id:
        admin = Cliente.objects.get(tipo_conta="admin", id=id)

    if request.method == "POST":
        form = AdminForm(request.POST)

        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.tipo_conta = "admin"
            cliente.save()
            assign_role(cliente, "admin")
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


#  ============================ PRATO ============================  #
@has_role_decorator("admin")
def criar_editar_prato(request, id=None):
    prato = None

    if id:
        prato = Prato.objects.get(id=id)

    if request.method == "POST":
        form = PratoForm(request.POST, request.FILES, instance=prato)

        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = PratoForm(instance=prato)

    return render(request, "models/forms/form.html", {"form": form, "prato": prato})


@has_role_decorator("admin")
def gerenciar_pratos(request):
    pratos = Prato.objects.all()
    return render(
        request,
        "models/admin_gerente/gerencia_pratos.html",
        {"pratos": pratos, "pg": "prato"},
    )


@has_role_decorator("admin")
def deletar_prato(request, id):
    Prato.objects.get(id=id).delete()
    return redirect("gerenciar_prato")


#  ============================ COZINHA ============================  #
@has_role_decorator("admin")
def gerenciar_cozinhas(request):
    return render(
        request,
        "models/admin_gerente/gerencia.html",
        {"clientes": Cozinha.objects.all(), "pg": "cozinha"},
    )


@has_role_decorator("admin")
def deletar_cozinha(request, id):
    Cozinha.objects.get(id=id).delete()
    return redirect("gerenciar_cozinhas")


@has_role_decorator("admin")
def criar_editar_cozinha(request, id=None):
    cozinha = None
    if id:
        cozinha = Cozinha.objects.get(id=id)

    if request.method == "POST":
        form = CozinhaForm(request.POST)
        if form.is_valid():
            caixa = form.save(commit=False)
            caixa.tipo_conta = "Cozinha"
            caixa.save()
            assign_role(caixa, "cozinha")

            return redirect("home_admin")
    else:
        form = CozinhaForm(instance=cozinha)

    return render(request, "models/forms/form.html", {"form": form})


#  ============================ GARCOM ============================  #
@has_role_decorator("admin")
def gerenciar_garcons(request):
    return render(
        request,
        "models/admin_gerente/gerencia.html",
        {"clientes": Garcom.objects.all(), "pg": "garcom"},
    )


@has_role_decorator("admin")
def deletar_garcom(request, id):
    Garcom.objects.get(id=id).delete()
    return render(
        request,
        "models/admin_gerente/gerencia.html",
        {"clientes": Garcom.objects.all()},
    )


@has_role_decorator("admin")
def criar_editar_garcom(request, id=None):
    garcom = None

    if id:
        garcom = Garcom.objects.get(id=id)

    if request.method == "POST":
        form = GarcomForm(request.POST)
        if form.is_valid():
            garcom = form.save(commit=False)
            garcom.tipo_conta = "Garcom"
            garcom.save()
            assign_role(garcom, "garcom")

            return redirect("home_admin")
    else:
        form = GarcomForm(instance=garcom)

    return render(request, "models/forms/form.html", {"form": form})


#  ============================ CAIXA ============================  #
@has_role_decorator("admin")
def deletar_caixa(request, id):
    Caixa.objects.get(id=id).delete()
    return render(
        request, "models/admin_gerente/gerencia.html", {"clientes": Caixa.objects.all()}
    )


@has_role_decorator("admin")
def gerenciar_caixas(request):
    return render(
        request,
        "models/admin_gerente/gerencia.html",
        {"clientes": Caixa.objects.all(), "pg": "caixa"},
    )


@has_role_decorator("admin")
def criar_editar_caixa(request, id=None):
    caixa = None

    if id:
        caixa = Caixa.objects.get(id=id)

    if request.method == "POST":
        form = CaixaForm(request.POST)
        if form.is_valid():
            caixa = form.save(commit=False)
            caixa.tipo_conta = "Caixa"
            caixa.save()
            assign_role(caixa, "caixa")

            return redirect("home_admin")
    else:
        form = CaixaForm(instance=caixa)

    return render(request, "models/forms/form.html", {"form": form})


#  ============================ CLIENTE ============================  #
@has_role_decorator("admin")
def editar_cliente(request, id):
    cliente = Cliente.objects.get(id=id)

    if request.method == "POST":
        if form.is_valid():
            form.save()

            return redirect("gerenciar_clientes")
    else:
        form = ClienteFormAdmin(instance=cliente)
    return render(request, "models/forms/form.html", {"form": form, "cliente": cliente})


@has_role_decorator("admin")
def deletar_cliente(request, id):
    Cliente.objects.get(id=id).delete()
    return render(
        request,
        "models/admin_gerente/gerencia.html",
        {"clientes": Cliente.objects.all()},
    )


@has_role_decorator("admin")
def gerenciar_clientes(request):
    return render(
        request,
        "models/admin_gerente/gerencia.html",
        {"clientes": Cliente.objects.filter(tipo_conta="Cliente"), "pg": "cliente"},
    )


#  ============================ ADICIONAL ============================  #
@has_role_decorator("admin")
def criar_editar_adicional(request, id=None):
    adicional = None

    if id:
        adicional = Adicional.objects.get(id=id)

    if request.method == "POST":
        form = AdicionalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = AdicionalForm(instance=adicional)
    return render(request, "models/forms/form.html", {"form": form, "adicional":adicional})


@has_role_decorator("admin")
def deletar_adicional(request, id):
    Adicional.objects.get(id=id).delete()
    return redirect("gerenciar_adicionais")


@has_role_decorator("admin")
def gerenciar_adicionais(request):
    context = {
        "adicionais": Adicional.objects.all(),
        "pg": "adicional",
    }

    return render(request, "models/admin_gerente/gerencia_adicionais.html", context)
