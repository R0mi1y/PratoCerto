
from django.shortcuts import redirect, render, get_object_or_404
from pedidos.models import Pedido, PedidoPrato

def home(request):
    pedidos = Pedido.objects.all()
    contexto = {
            'pedidos': []
    }
    
    for pedido in pedidos:
        pedidoPrato = PedidoPrato.objects.filter(pedido=pedido) 
        contexto['pedidos'].append([pedido, pedidoPrato])
    
    return render(request, 'models/cozinhas/home_cozinha.html', contexto)


def pedido_pronto(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.pronto = True
    pedido.save()
    # Realizar notificação ao garçom, por exemplo, através de uma mensagem flash
    return redirect('home')
