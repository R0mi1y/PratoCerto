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
        pedidoPrato_form = PedidoPratoForm(request.POST, prato_id=id)
        
        if pedidoPrato_form.is_valid():
            pedidoPrato = pedidoPrato_form.save(commit=False)
            pedidoPrato.cliente = cliente
            pedidoPrato.save()
            
            return redirect('home')
    else:
        prato_form = PedidoPratoForm(prato_id=id)
        
    context = {
        'prato_form' : prato_form,
        'prato'      : prato,
        'comentarios': prato.comentarios.all(),
    }
    
    if Cliente.objects.get(user=request.user).tipo_conta == "Cliente":
        return render(request, "models/pedidos/fazer_pedido.html", context)
    elif Cliente.objects.get(user=request.user).tipo_conta == "Garcom":
        return render(request, "models/garcons/fazer_pedido.html", context)


@login_required
def criar_reserva(request):
    cliente = Cliente.objects.get(user_id=request.user.pk)
    if request.method == 'POST':
        form = ReservaForm(request.POST, cliente_id=cliente.pk)
        if form.is_valid():
            reserva = form.save()
            # Fazer algo com a reserva salva, como redirecionar para uma página de sucesso
            return redirect('home')
    return render(request, 'models/pedidos/fazer_reserva.html', {'form': ReservaForm(cliente_id=cliente.pk), "preco": 20.00, 'cadeiras_mesa': 4})
