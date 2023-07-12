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

    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        valor_pago = request.POST.get('valor_pago')

        pedido = get_object_or_404(Pedido, id=pedido_id)

        if decimal.Decimal(valor_pago) >= pedido.total:
            pedido.status = 'Pago'
            pedido.save()

            troco = decimal.Decimal(valor_pago) - pedido.total
            troco = round(troco, 2)

            # Define o valor de 'troco' na sessão
            request.session['troco'] = str(troco)

            # Redireciona para a mesma página para limpar os valores anteriores
            return redirect('home')

    elif request.method == 'GET':
        pedido_id = request.GET.get('pedido_id')
        if pedido_id:
            pedido = get_object_or_404(Pedido, id=pedido_id)

        # Remove o valor de 'troco' da sessão
        if 'troco' in request.session:
            del request.session['troco']

    contexto = {
        'pedido': pedido,
        'troco': troco
    }

    return render(request, 'models/caixas/home_caixa.html', contexto)





def historico_pedidos(request):
    hoje = timezone.now().date()
    
    # Obter histórico diário
    pedidos_pagos = Pedido.objects.filter(status='Pago')
    historico_diario = []
    
    for pedido in pedidos_pagos:
        data_pedido = timezone.localtime(pedido.data_pedido).date()
        if data_pedido == hoje:
            historico_diario.append(pedido)
    
    # Obter histórico mensal
    historico_mensal = []
    primeiro_dia_mes = hoje.replace(day=1)
    ultimo_dia_mes = primeiro_dia_mes + timedelta(days=31)
    pedidos_mensais = Pedido.objects.filter(status='Pago', data_pedido__range=(primeiro_dia_mes, ultimo_dia_mes))
    
    for pedido in pedidos_mensais:
        data_pedido = timezone.localtime(pedido.data_pedido).date()
        if primeiro_dia_mes <= data_pedido <= ultimo_dia_mes:
            historico_mensal.append(pedido)

    contexto = {
        'historico_diario': historico_diario,
        'historico_mensal': historico_mensal,
        'hoje': hoje,
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
        if id:
            garcom = Garcom.objects.get(id=id)
            
            garcom.password = make_password(request.POST.get("password"))
            garcom.cpf = request.POST.get('cpf')
            garcom.telefone = request.POST.get('telefone')
            garcom.email = request.POST.get('email')
            garcom.tipo_conta = "Garcom"
            garcom.save()
            
            assign_role(garcom, "garcom")
            
            return redirect("home_admin")
        form = CaixaForm(request.POST)
        if form.is_valid():
            caixa = form.save(commit=False)
            caixa.tipo_conta = "Caixa"
            caixa.save()
            assign_role(caixa, "caixa")

            return redirect("home_admin")
    else:
        form = CaixaForm(instance=caixa)

    return render(request, "models/forms/form.html", {"form": form, "titulo":"Cadastro do Caixa"})

