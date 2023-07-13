from django.http import JsonResponse
from pedidos.models import PedidoPrato

def notificacoes(request):
    status_pedido = PedidoPrato.objects.filter(cliente=request.user).exclude(status="Pago")
    
    lista = []
    for i in status_pedido:
        lista.append({"status":i.status, "prato":i.prato.nome})
    
    context = {
        'status_pedido': lista
    }
    
    return JsonResponse(context)
