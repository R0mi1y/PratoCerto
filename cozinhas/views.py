from django.shortcuts import redirect, render, get_object_or_404
from pedidos.models import PedidoPrato
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator
from .models import *
from .forms import *
from pratos.models import Ingrediente, Receita, IngredienteReceita



def home(request):
    pedidos_restaurante = PedidoPrato.objects.filter(status='Pendente local')
    pedidos_site = PedidoPrato.objects.filter(status='Pendente')
    ingredientes = Ingrediente.objects.all()
    receitas = Receita.objects.all()
    ingredientes_receita = IngredienteReceita.objects.all()
    contexto = {
        'pedidos_restaurante': pedidos_restaurante,
        'pedidos_site': pedidos_site,
        'ingredientes': ingredientes,
        'receitas': receitas,
        'ingredientes_receita': ingredientes_receita,
    }
    
    return render(request, 'models/cozinhas/home_cozinha.html', contexto)


def pedido_pronto(request, pedido_id):
    pedidoPrato = get_object_or_404(PedidoPrato, id=pedido_id)
    pedidoPrato.status = "pronto para entrega"
    pedidoPrato.save()
    # Realizar notificação ao garçom, por exemplo, através de uma mensagem flash
    return redirect('home_cozinha')


#  ============================ COZINHA CRUD ============================  #
@has_role_decorator("admin")
def gerenciar_cozinhas(request):
    return render(
        request,
        "models/admin_gerente/gerencia.html",
        {"clientes": Cozinha.objects.all(), "pg": "cozinha"},
    )


@has_role_decorator("admin")
def deletar_cozinha(request, id):
    Cozinha.objects.get(id=id).delete()
    return redirect("gerenciar_cozinhas")


@has_role_decorator("admin")
def criar_editar_cozinha(request, id=None):
    cozinha = None
    if id:
        cozinha = Cozinha.objects.get(id=id)

    if request.method == "POST":
        form = CozinhaForm(request.POST, instance=cozinha)
        if form.is_valid():
            caixa = form.save(commit=False)
            caixa.tipo_conta = "Cozinha"
            caixa.save()
            assign_role(caixa, "cozinha")

            return redirect("home_admin")
    else:
        form = CozinhaForm(instance=cozinha)

    return render(request, "models/forms/form.html", {"form": form})
