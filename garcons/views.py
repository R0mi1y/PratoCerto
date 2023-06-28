from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from pratos.models import Prato
from pedidos.models import Mesa, Pedido
from .forms import PedidoForm
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


# def fazer_pedido(request):
#     if request.method == 'POST':
#         form = PedidoForm(request.POST)
#         if form.is_valid():
#             pedido = form.save()
#             # Fazer algo com o pedido salvo, como redirecionar para uma página de sucesso
#     else:
#         form = PedidoForm()
    
#     return render(request, 'models/garcons/fazer_pedido.html', {'form': form})


@login_required
def fazer_pedido(request, id):
    prato = Prato.objects.get(id=id)

    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        prato_form = PedidoPratoForm(request.POST, prato_id=id)
        if pedido_form.is_valid() and prato_form.is_valid():
            pedido = pedido_form.save()
            prato = prato_form.save(commit=False)
            prato.pedido = pedido
            prato.save()
            
            return redirect('home')
    else:
        pedido_form = PedidoForm()
        prato_form = PedidoPratoForm(prato_id=id)
        
    context = {
        'pedido_form': pedido_form,
        'prato_form' : prato_form,
        'prato'      : prato,
    }
    
    return render(request, 'models/garcons/fazer_pedido.html', context)