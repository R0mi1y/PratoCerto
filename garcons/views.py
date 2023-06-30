from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from clientes.models import Cliente
from pratos.models import Prato
from pedidos.models import Mesa, Pedido
from pedidos.forms import GarcomPedidoForm
from PratoCerto.settings import AUX
from .forms import *

@login_required
def home(request):
    # Recupera todas as mesas disponíveis
    tables = Mesa.objects.all()

    # Recupera os pedidos em andamento
    orders = Pedido.objects.all()

    context = {
        'tables': tables,
        'orders': orders
    }
    context["Categorias"] = AUX["Categorias"]

    return render(request, 'models/garcons/home.html', context)


@login_required
def fazer_pedido(request, id):
    cliente = Cliente.objects.get(user=request.user.id)
    prato = Prato.objects.get(id=id)

    if request.method == 'POST':
        pedidoPrato_form = PedidoPratoGarcomForm(request.POST, prato_id=id)

        if pedidoPrato_form.is_valid():
            pedidoPrato = pedidoPrato_form.save(commit=False)
            pedidoPrato.status = "carrinho garcom " + cliente.user.username
            
            if pedidoPrato.nome_cliente.replace(".", "").replace("-", "").isdigit():
                pedidoPrato.cliente = Cliente.objects.get(cpf=pedidoPrato.nome_cliente)
                pedidoPrato.nome_cliente = pedidoPrato.cliente.user.username
                
            pedidoPrato.save()

            return redirect("home")
    else:
        prato_form = PedidoPratoGarcomForm(prato_id=id)
        
    context = {
        'prato_form' : prato_form,
        'prato'      : prato,
    }
    
    return render(request, 'models/garcons/fazer_pedido.html', context)


@login_required
def ver_carrinho(request):
    cliente = Cliente.objects.get(user=request.user.id)
    status = "carrinho garcom " + cliente.user.username

    context = {
        "pedidos": PedidoPrato.objects.filter(status=status)
    }
    
    return render(request, 'models/garcons/carrinho.html', context)


@login_required
def comprar_carrinho(request):
    cliente = Cliente.objects.get(user=request.user.id)
    pedidosPrato = PedidoPrato.objects.filter(cliente=cliente, status="no Carrinho")
    
    if request.method == "POST":
        form = GarcomPedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cliente = cliente
            total = 0
            
            for pedidoPrato in pedidosPrato:
                total += pedidoPrato.prato.preco * pedidoPrato.quantidade
                pedidoPrato.status = "Pendente"
                pedidoPrato.pedido = pedido
                
            pedido.total = total
            pedido.save()
            
            [pedidoPrato.save() for pedidoPrato in pedidosPrato]
            
            return redirect("ver pedidos")

    context = {
        "pedidos": pedidosPrato,
        "form": GarcomPedidoForm(),
    }
    
    return render(request, 'models/pedidos/pagamento.html', context)
