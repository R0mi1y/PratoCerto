from django.http import JsonResponse
from pedidos.models import Pedido
from django.core import serializers
from django.forms.models import model_to_dict

def atualizar_pedido(request):
    pedidos = Pedido.objects.all()
    array = []
    
    for pedido in pedidos:
        array.append(model_to_dict(pedido))
    
    return JsonResponse({'pedidos':array})
