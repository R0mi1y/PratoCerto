from django.forms import model_to_dict
from django.http import JsonResponse
from pedidos.models import Pedido, PedidoPrato


def get_pedidoPrato(request, status):
    status = status.replace('_', ' ')
    pedidoPrato_prontos = PedidoPrato.objects.filter(status=status)
    pedidoPratos_array = []

    for pedidoPrato in pedidoPrato_prontos:
        pedidoPratoDic = {
            'pedidoPrato': {
                "observacao":pedidoPrato.observacao,
                "nome_cliente":pedidoPrato.nome_cliente,
                "status":pedidoPrato.status,
                "quantidade":pedidoPrato.quantidade,
                "id":pedidoPrato.id
                },
            'pedido': model_to_dict(pedidoPrato.pedido),
            'prato': {
                'foto': pedidoPrato.prato.foto.url,
                'nome': pedidoPrato.prato.nome,
            }
        }
        pedidoPratoDic['pedido']['mesa'] = None
        pedidoPratoDic['pedido']['endereco'] = None
        if pedidoPrato.pedido.mesa_id:
            pedidoPratoDic['pedido']['mesa'] = model_to_dict(pedidoPrato.pedido.mesa)
            
        elif pedidoPrato.pedido.endereco_id:
            pedidoPratoDic['pedido']['endereco'] = model_to_dict(pedidoPrato.pedido.endereco)
            
        pedidoPratos_array.append(pedidoPratoDic)
    
    return JsonResponse({"pedidoPrato_prontos": pedidoPratos_array})



def get_pedidos(request, status):
    status = status.replace('_', ' ')
    pedidos = Pedido.objects.filter(status=status)
    pedido_array = []

    for pedido in pedidos:
        pedidoPratoDic = {
            'pedido': model_to_dict(pedido),
        }
        pedido_array.append(pedidoPratoDic)
    
    return JsonResponse({"pedido_prontos": pedido_array, "status": status})
