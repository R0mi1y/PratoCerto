from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from clientes.models import Cliente
from pratos.models import *
from pedidos.models import Mesa, Pedido, PedidoPrato
from pedidos.forms import GarcomPedidoForm
from PratoCerto.settings import AUX
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required, user_passes_test
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator


@has_role_decorator("garcom")
def home(request):
    tables = Mesa.objects.all()
    orders = Pedido.objects.all()

    # Filtra os PedidoPrato com status pronto para entrega
    pedidoPrato_prontos = PedidoPrato.objects.filter(status='pronto para entrega')
    pedidos_para_entrega = Pedido.objects.filter(status="Em rota de entrega")
    
    context = {
        'tables': tables,
        'orders': orders,
        'pedidoPrato_prontos': pedidoPrato_prontos,  # Adiciona os PedidoPrato prontos ao contexto
        'pedidos_para_entrega': pedidos_para_entrega
    }
    context["Categorias"] = AUX["Categorias"]

    return render(request, 'models/garcons/home.html', context)


@has_role_decorator("garcom")
def fazer_pedido(request, id):
    cliente = request.user
    prato = Prato.objects.get(id=id)

    if request.method == 'POST':
        pedidoPrato_form = PedidoPratoGarcomForm(request.POST, prato_id=id)

        if pedidoPrato_form.is_valid():
            pedidoPrato = pedidoPrato_form.save(commit=False)
            pedidoPrato.status = "carrinho garcom " + cliente.username
            
            if pedidoPrato.nome_cliente.replace(".", "").replace("-", "").isdigit():
                pedidoPrato.cliente = Cliente.objects.get(cpf=pedidoPrato.nome_cliente)
                pedidoPrato.nome_cliente = pedidoPrato.cliente.username
                
            pedidoPrato.save()
            
            for id in request.POST.getlist("adicional"):
                adicional = Adicional.objects.get(id=id)
                pedidoPrato.adicional.add(adicional)
            
            pedidoPrato.save()

            return redirect("home_garcom")
    else:
        prato_form = PedidoPratoGarcomForm(prato_id=id)
        
    context = {
        'prato_form' : prato_form,
        'prato'      : prato,
    }
    
    return render(request, 'models/garcons/fazer_pedido.html', context)


@has_role_decorator("garcom")
def ver_carrinho(request):
    cliente = request.user
    status = "carrinho garcom " + cliente.username

    context = {
        "pedidos": PedidoPrato.objects.filter(status=status)
    }
    
    return render(request, 'models/garcons/carrinho.html', context)


@has_role_decorator("garcom")
def comprar_carrinho(request):
    cliente = request.user
    pedidosPrato = PedidoPrato.objects.filter(status="carrinho garcom " + cliente.username)
    
    total = 0
    if request.method == "POST":
        form = GarcomPedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cliente = cliente
            
            for pedidoPrato in pedidosPrato:
                total += pedidoPrato.prato.preco * pedidoPrato.quantidade
                pedidoPrato.status = "Pendente local"
                pedidoPrato.pedido = pedido
                
            pedido.total = total
            pedido.save()
            
            [pedidoPrato.save() for pedidoPrato in pedidosPrato]
            
            return redirect("ver_pedidos_garcom")

    for pedidoPrato in pedidosPrato:
        total += pedidoPrato.prato.preco * pedidoPrato.quantidade
                
    context = {
        "pedidos": pedidosPrato,
        "form": GarcomPedidoForm(),
        "total": total,
    }
    
    return render(request, 'models/pedidos/pagamento_garcom.html', context)


@has_role_decorator("garcom")
def ver_pedidos(request):
    cliente = request.user

    context = {
        "pedidos": Pedido.objects.filter(cliente=cliente).exclude(status="no Carrinho")
    }
    
    return render(request, 'models/clientes/pedidos.html', context)


def servir_pedido(request, pedido_prato_id):
    pedido_prato = get_object_or_404(PedidoPrato, id=pedido_prato_id)
    # Alterar o status do PedidoPrato para "sendo servido"
    pedido_prato.status = "servido"
    pedido_prato.save()
    
    pedido = pedido_prato.pedido
    if len(PedidoPrato.objects.filter(pedido=pedido).exclude(status="servido")) == 0:
        pedido.status = "Pendente local pagamento"
        pedido.save()
    
    return redirect("home_garcom")


def servir_pedido_site(request, pedido_prato_id):
    pedido_prato = get_object_or_404(PedidoPrato, id=pedido_prato_id)
    
    pedido_prato.status = "servido"
    pedido_prato.save()
    
    pedido = pedido_prato.pedido
    if len(PedidoPrato.objects.filter(pedido=pedido).exclude(status="servido")) == 0:
        pedido.status = "Em rota de entrega"
        pedido.save()
    
    return redirect("home_garcom")


@has_role_decorator("garcom")
def remover_carrinho(request, id):
    pedido = get_object_or_404(PedidoPrato, id=id)
    pedido.delete()
    
    return redirect("ver_carrinho_garcom")


@has_role_decorator("garcom")
def editar_carrinho(request, id):
    cliente = request.user
    pedidoPrato = PedidoPrato.objects.get(id=id)
    
    if request.method == "POST":
        form = PedidoPratoGarcomForm(request.POST, prato_id=pedidoPrato.prato.pk, instance=pedidoPrato)
        if form.is_valid():
            pedidoPrato = form.save(commit=False)
            pedidoPrato.cliente = cliente
            pedidoPrato.save()
            
            return redirect("ver_carrinho_garcom")
        
    context = {
        'prato_form' : PedidoPratoGarcomForm(instance=pedidoPrato, prato_id=pedidoPrato.prato.pk),
        'prato'      : pedidoPrato.prato,
        'comentarios': pedidoPrato.prato.comentarios.all(),
    }
    return render(request, 'models/pedidos/fazer_pedido.html', context)


#  ============================ GARCOM CRUD ============================  #
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
        form = GarcomForm(request.POST, instance=garcom)
        if form.is_valid():
            garcom = form.save(commit=False)
            garcom.tipo_conta = "Garcom"
            garcom.save()
            assign_role(garcom, "garcom")

            return redirect("home_admin")
    else:
        form = GarcomForm(instance=garcom)

    return render(request, "models/forms/form.html", {"form": form, "titulo":"Formulário de Garçom"})


def entregar(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.status = "Entregue"
    pedido.save()
    
    return redirect("home_garcom")