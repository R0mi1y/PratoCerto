import mercadopago
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from mercadopago import MP
from django.conf import settings
from django.shortcuts import redirect
from pedidos.models import PedidoPrato, Pedido
from django.http import HttpResponse


def pagar_pedido(request, pedido, valor_preco_pontos=None):
    preference = {
        "items": [],
        "back_urls": {
            "success": f"http://localhost:8000/pagamentos/pedido/sucesso/",
            "failure": "http://localhost:8000/",
            "pending": "http://localhost:8000/"
        }
    }
    if valor_preco_pontos:
        preference["items"].append({
          "title": "Frete",
          "quantity": 1,
          "currency_id": "BRL",
          "unit_price": float(settings.CACHED_CATEGORIES['frete_entrega']) - float(valor_preco_pontos)
    })
    else:
        preference["items"].append({
            "title": "Frete",
            "quantity": 1,
            "currency_id": "BRL",
            "unit_price": float(settings.CACHED_CATEGORIES['frete_entrega'])
        })
    pedidoprato_set = PedidoPrato.objects.filter(pedido=pedido)
    for pedidoPrato in pedidoprato_set:
        preference["items"].append({
          "title": pedidoPrato.prato.nome,
          "quantity": int(pedidoPrato.quantidade),
          "currency_id": "BRL",
          "unit_price": float(pedidoPrato.prato.preco)
        })
        
    mp = mercadopago.MP(settings.CLIENT_ID, settings.CLIENT_SECRET)
    preferenceResult = mp.create_preference(preference)

    url = preferenceResult["response"]["init_point"]
    
    pedido.id_pagamento = preferenceResult["response"]["id"]
    pedido.save()
    
    return redirect(url)


def pagar_reserva(request, valor):
    preference = {
        "items": [{
          "title": "Reserva da mesa",
          "quantity": 1,
          "currency_id": "BRL",
          "unit_price": float(valor),
        }],
        "back_urls": {
            "success": f"http://localhost:8000/pagamentos/pedido/sucesso/",
            "failure": "http://localhost:8000/",
            "pending": "http://localhost:8000/"
        },
    }
        
    mp = mercadopago.MP(settings.CLIENT_ID, settings.CLIENT_SECRET)

    preferenceResult = mp.create_preference(preference)

    url = preferenceResult["response"]["init_point"]
    
    return redirect(url)


@csrf_exempt
def retorno_mercadopago(request):
    if request.method == 'POST':
        # Obter os dados da notificação do MercadoPago
        payment_id = request.POST.get('id')
        
        # Consultar a API do MercadoPago para obter informações sobre o pagamento
        mp = mercadopago.MP(settings.CLIENT_ID, settings.CLIENT_SECRET)
        payment_info = mp.get_payment_info(payment_id)
        
        # Verificar o estado do pagamento
        payment_status = payment_info['status']
        
        # Realizar as ações necessárias com base no estado do pagamento
        if payment_status == 'approved':
            pedido = Pedido.objects.get(payment_status=payment_id)
            
            pedido.cliente = cliente
            total = 0
            if pedido.local_retirada == "entrega":
                pedido.taxa_entrega = settings.CACHED_CATEGORIES["frete_entrega"]
                total += pedido.taxa_entrega
            else:
                pedido.taxa_entrega = 0
            
            pedidosPrato = PedidoPrato.objects.filter(pedido=pedido)
                
            for pedidoPrato in pedidosPrato:
                total += pedidoPrato.prato.preco * pedidoPrato.quantidade
                pedidoPrato.status = "Pago"
                pedidoPrato.pedido = pedido
                
            pedido.total = total
            
            if len(PedidoPrato.objects.filter(pedido=pedido).exclude(status="Pago")) == 0:
                pedido.status = "Pago"
                
            
            pedido.save()
            
            [pedidoPrato.save() for pedidoPrato in pedidosPrato]
            return HttpResponse('Pagamento aprovado')
    else:
        return HttpResponse(status=405)
