from django.shortcuts import render, redirect
from clientes.models import Cliente
from .forms import *
from pratos.models import Prato, Comentario
from django.contrib.auth.decorators import login_required


@login_required
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
            
            if pedido.local_retirada == "reserva":
                request.session["pedido"] = pedido.pk
                return render(request, 'models/pedidos/fazer_reserva.html', {'form': ReservaForm(cliente_id=cliente.pk), "preco": 20.00, 'cadeiras_mesa': 4})
            else:
                return redirect('home')
    else:
        pedido_form = PedidoForm(cliente_id=cliente.pk)
        prato_form = PedidoPratoForm(prato_id=id)
        
    context = {
        'pedido_form': pedido_form,
        'prato_form' : prato_form,
        'prato'      : prato,
        'comentarios': prato.comentarios.all(),
    }
    
    return render(request, 'models/pedidos/fazer_pedido.html', context)


@login_required
def reserva_create(request):
    pedido = request.session.get('pedido', None)
    cliente = Cliente.objects.get(user_id=request.user.pk)
    if request.method == 'POST':
        form = ReservaForm(request.POST, cliente_id=cliente.pk, pedido_id=pedido)
        if form.is_valid():
            reserva = form.save()
            # Fazer algo com a reserva salva, como redirecionar para uma página de sucesso
    
    return redirect('home')
