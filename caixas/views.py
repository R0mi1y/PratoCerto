from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, get_object_or_404
from pedidos.models import Pedido
from django.utils import timezone


def home(request):
    pedido = None

    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        valor_pago = request.POST.get('valor_pago')
        
        pedido = get_object_or_404(Pedido, id=pedido_id)

        if float(valor_pago) >= pedido.total:
            pedido.status = 'Pago'
            pedido.save()
        else:
            mensagem = "Não é possível concluir a operação. O valor é inferior ao valor total do pedido."
            contexto = {
                'pedido': pedido,
                'mensagem': mensagem
            }
            return render(request, 'models/caixas/home_caixa.html', contexto)

    elif request.method == 'GET':
        pedido_id = request.GET.get('pedido_id')
        if pedido_id:
            pedido = get_object_or_404(Pedido, id=pedido_id)
            
    contexto = {
        'pedido': pedido
    }
    
    return render(request, 'models/caixas/home_caixa.html', contexto)


def pedidos_hoje(request):
    # Obter pedidos pendentes
    pedidos_pendentes = Pedido.objects.filter(status='Pendente')
    hoje = timezone.now().date()
    # Obter histórico diário
    pedidos_pagos = Pedido.objects.filter(status='Pago')
    historico_diario = []
    
    for pedido in pedidos_pagos:
        data_pedido = timezone.localtime(pedido.data_pedido).date()
        if data_pedido == hoje:
            historico_diario.append(pedido)

    contexto = {
        'pedidos_pendentes': pedidos_pendentes,
        'historico_diario': historico_diario,
        'hoje':hoje,
    }

    return render(request, 'models/caixas/pedidos.html', contexto)


