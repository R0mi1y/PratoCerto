from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from clientes.models import Cliente
from pratos.models import Prato
from pedidos.models import Mesa, Pedido, PedidoPrato
from pedidos.forms import GarcomPedidoForm
from PratoCerto.settings import AUX
from .forms import *
from django.shortcuts import get_object_or_404


@login_required
def home(request):
    tables = Mesa.objects.all()
    orders = Pedido.objects.all()

    # Filtra os PedidoPrato com status pronto para entrega
    pedidoPrato_prontos = PedidoPrato.objects.filter(status='pronto para entrega')

    context = {
        'tables': tables,
        'orders': orders,
        'pedidoPrato_prontos': pedidoPrato_prontos,  # Adiciona os PedidoPrato prontos ao contexto
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
    pedidosPrato = PedidoPrato.objects.filter(status="carrinho garcom " + request.user.username)
    
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

def servir_pedido(request, pedido_prato_id):
    
    pedido_prato = get_object_or_404(PedidoPrato, id=pedido_prato_id)

    # Alterar o status do PedidoPrato para "sendo servido"
    pedido_prato.status = "sendo servido"
    pedido_prato.save()
