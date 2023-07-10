from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from mercadopago import MP
from PratoCerto import settings

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
        return render(request, 'models/pagamentos/pagamento.html')
