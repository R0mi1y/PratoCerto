from django.shortcuts import render
from pedidos.models import Mesa, Pedido

def home(request):
    # Recupera todas as mesas disponíveis
    tables = Mesa.objects.all()

    # Recupera os pedidos em andamento
    orders = Pedido.objects.filter(status='Em andamento')

    context = {
        'tables': tables,
        'orders': orders
    }

    return render(request, 'models/garcons/home.html', context)
