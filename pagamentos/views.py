import mercadopago
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from mercadopago import MP
from django.conf import settings
from django.shortcuts import redirect
from pedidos.models import PedidoPrato
from django.http import HttpResponse

def teste1(request):
    pass




def pagar_pedido(request, pedido):
    preference = {
      "items": [
          {
          "title": "pedidoPrato.prato.nome",
          "quantity": 2,
          "currency_id": "BRL",
          "unit_price": 23
        },
          {
          "title": "pedidoPrato.prato.nome",
          "quantity": 2,
          "currency_id": "BRL",
          "unit_price": 23
        }
      ]
    }
    # pedidoprato_set = PedidoPrato.objects.filter(pedido=pedido)
    # for pedidoPrato in pedidoprato_set:
    #     preference["items"].append({
    #       "title": pedidoPrato.prato.nome,
    #       "quantity": pedidoPrato.quantidade,
    #       "currency_id": "BRL",
    #       "unit_price": calcularPrecoPedidoPrato(pedidoPrato)
    #     })

    mp = mercadopago.MP(settings.CLIENT_ID, settings.CLIENT_SECRET)

    preferenceResult = mp.create_preference(preference)

    url = preferenceResult["response"]["init_point"]
    
    return redirect(url)


def calcularPrecoPedidoPrato(pedidoPrato):
    total = 0
    total += pedidoPrato.prato * pedidoPrato.quantidade
    
    for adicional in pedidoPrato.adicional.all():
        total += adicional.preco
    
    return total
    











@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        mp = MP(access_token=settings.MERCADOPAGO_ACCESS_TOKEN)

        payment_data = {
            'transaction_amount': 1000,  # Valor em centavos (R$ 10,00)
            'token': request.POST.get('token'),
            'description': 'Exemplo de pagamento',
            'payment_method_id': request.POST.get('payment_method_id'),
            'payer': {
                'email': request.POST.get('cardholderEmail')
            }
        }

        response = mp.post("/v1/payments", payment_data)
        if response['status'] == 201:
            # Pagamento bem-sucedido
            return render(request, 'payment_success.html')
        else:
            # Lidar com erros de pagamento
            error_message = response['response']['message']
            return render(request, 'payment_error.html', {'error': error_message})
    else:
        return render(request, 'models/pagamentos/pagamento.html', {"PUBLIC_KEY":settings.MERCADOPAGO_PUBLIC_KEY})


@csrf_exempt
def process_payment_all(request):
    if request.method == 'POST':
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

        payment_data = {
            "transaction_amount": float(request.POST.get("transaction_amount")),
            "token": request.POST.get("token"),
            "description": request.POST.get("description"),
            "installments": int(request.POST.get("installments")),
            "payment_method_id": request.POST.get("payment_method_id"),
            "payer": {
                "email": request.POST.get("cardholderEmail"),
                "identification": {
                    "type": request.POST.get("identificationType"),
                    "number": request.POST.get("identificationNumber")
                },
                "first_name": request.POST.get("cardholderName")
            }
        }
        
        preference_response = sdk.preference().create(preference_data)
        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]
        print(payment)
    else:
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        preference = preference_response["response"]
        
        return render(request, 'models/pagamentos/pagamento.html', {"PUBLIC_KEY":settings.MERCADOPAGO_PUBLIC_KEY, "PREFERENCE_ID": preference})

