from django.shortcuts import render, redirect
from clientes.models import Cliente
from .forms import *
from pratos.models import Prato


def fazer_pedido(request, id):
    cliente = Cliente.objects.get(user_id=request.user.pk)
    prato = Prato.objects.get(id=id)

    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST, cliente_id=cliente.pk)
        prato_form = PedidoPratoForm(request.POST, prato_id=id)
        if pedido_form.is_valid() and prato_form.is_valid():
            pedido = pedido_form.save()
            prato = prato_form.save(commit=False)
            prato.pedido = pedido
            prato.save()
            return redirect('sucesso')
    else:
        pedido_form = PedidoForm(cliente_id=cliente.pk)
        prato_form = PedidoPratoForm(prato_id=id)
    
    context = {
        'pedido_form': pedido_form,
        'prato_form': prato_form,
        'prato': prato
    }
    
    return render(request, 'models/pedidos/fazer_pedido.html', context)


def pedido_sucesso(request):
    return render(request, 'models/pedidos/pedido_sucesso.html')
