from django.shortcuts import redirect, render, get_object_or_404
from pedidos.models import PedidoPrato

def home(request):
    contexto = {
            'pedidos': PedidoPrato.objects.all()
    }
    
    return render(request, 'models/cozinhas/home_cozinha.html', contexto)


def pedido_pronto(request, pedido_id):
    pedidoPrato = get_object_or_404(PedidoPrato, id=pedido_id)
    pedidoPrato.status = "pronto para entrega"
    pedidoPrato.save()
    # Realizar notificação ao garçom, por exemplo, através de uma mensagem flash
    return redirect('home_cliente')
