from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, get_object_or_404
from pedidos.models import Pedido
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator
from .models import Caixa
from .forms import CaixaForm
from django.shortcuts import redirect
import decimal

# def home(request):
#     pedido = None

#     if request.method == 'POST':
#         pedido_id = request.POST.get('pedido_id')
#         valor_pago = request.POST.get('valor_pago')
        
#         pedido = get_object_or_404(Pedido, id=pedido_id)

#         if float(valor_pago) >= pedido.total:
#             pedido.status = 'Pago'
#             pedido.save()
#         else:
#             mensagem = "Não é possível concluir a operação. O valor é inferior ao valor total do pedido."
#             contexto = {
#                 'pedido': pedido,
#                 'mensagem': mensagem
#             }
#             return render(request, 'models/caixas/home_caixa.html', contexto)

#     elif request.method == 'GET':
#         pedido_id = request.GET.get('pedido_id')
#         if pedido_id:
#             pedido = get_object_or_404(Pedido, id=pedido_id)
            
#     contexto = {
#         'pedido': pedido
#     }
    
#     return render(request, 'models/caixas/home_caixa.html', contexto)
from django.shortcuts import redirect

def home(request):
    pedido = None
    troco = None
    
    contexto = {
        "troco": round(0, 2) ,
    }
    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        valor_pago = request.POST.get('valor_pago')
        request.method = "GET"
        
        pedido = get_object_or_404(Pedido, id=pedido_id)

        if decimal.Decimal(valor_pago) >= pedido.total:
            pedido.status = 'Finalizado'
            pedido.save()

            troco = decimal.Decimal(valor_pago) - pedido.total
            contexto['troco'] = round(troco, 2)
        
            # Redireciona para a mesma página para limpar os valores anteriores
            # return redirect('home')

    elif request.method == 'GET':
        pedido_id = request.GET.get('pedido_id')
        if pedido_id:
            pedido = get_object_or_404(Pedido, id=pedido_id)

    contexto['pedido'] = pedido

    return render(request, 'models/caixas/home_caixa.html', contexto)


def historico_pedidos(request):
    hoje = timezone.now().date()
    
    # Obter histórico diário
    pedidos_pagos = Pedido.objects.filter(status='Finalizado')
    historico_diario = []
    total_diario = 0  # Variável para calcular a quantidade arrecadada do dia
    
    for pedido in pedidos_pagos:
        data_pedido = timezone.localtime(pedido.data_pedido).date()
        if data_pedido == hoje:
            historico_diario.append(pedido)
            total_diario += pedido.total
    
    # Obter histórico mensal
    historico_mensal = []
    total_mensal = 0  # Variável para calcular a quantidade arrecadada do mês
    primeiro_dia_mes = hoje.replace(day=1)
    ultimo_dia_mes = primeiro_dia_mes + timedelta(days=31)
    pedidos_mensais = Pedido.objects.filter(status='Finalizado', data_pedido__range=(primeiro_dia_mes, ultimo_dia_mes))
    
    for pedido in pedidos_mensais:
        data_pedido = timezone.localtime(pedido.data_pedido).date()
        if primeiro_dia_mes <= data_pedido <= ultimo_dia_mes:
            historico_mensal.append(pedido)
            total_mensal += pedido.total

    contexto = {
        'historico_diario': historico_diario,
        'historico_mensal': historico_mensal,
        'hoje': hoje,
        'total_diario': total_diario,
        'total_mensal': total_mensal,
    }

    return render(request, 'models/caixas/historico.html', contexto)


#  ============================ CAIXA CRUD ============================  #
@has_role_decorator("admin")
def deletar_caixa(request, id):
    Caixa.objects.get(id=id).delete()
    return render(
        request, "models/admin_gerente/gerencia.html", {"clientes": Caixa.objects.all()}
    )


@has_role_decorator("admin")
def gerenciar_caixas(request):
    return render(
        request,
        "models/admin_gerente/gerencia.html",
        {"clientes": Caixa.objects.all(), "pg": "caixa"},
    )


@has_role_decorator("admin")
def criar_editar_caixa(request, id=None):
    caixa = None

    if id:
        caixa = Caixa.objects.get(id=id)

    if request.method == "POST":
        form = CaixaForm(request.POST, instance=caixa)
        if form.is_valid():
            caixa = form.save(commit=False)
            caixa.tipo_conta = "Caixa"
            caixa.save()
            assign_role(caixa, "caixa")

            return redirect("home_admin")
    else:
        form = CaixaForm(instance=caixa)

    return render(request, "models/forms/form.html", {"form": form, "titulo":"Cadastro do Caixa"})

