from django.shortcuts import render, redirect
from .forms import *
from .models import *
from pratos.models import Prato, Comentario
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from pagamentos.views import pagar_reserva


def fazer_pedido(request, id):
    if request.user.is_authenticated:
        cliente = request.user
        prato = Prato.objects.get(id=id)

        if request.method == "POST":
            pedidoPrato_form = PedidoPratoForm(request.POST, prato_id=id)

            if pedidoPrato_form.is_valid():
                pedidoPrato = pedidoPrato_form.save(commit=False)
                pedidoPrato.cliente = cliente
                pedidoPrato.nome_cliente = cliente.username
                
                for id in request.POST.getlist("adicional"):
                    adicional = Adicional.objects.get(id=id)
                    pedidoPrato.adicional.add(adicional)
                pedidoPrato.save()

                return redirect("home")
        else:
            prato_form = PedidoPratoForm(prato_id=id)

        context = {
            "prato_form": prato_form,
            "prato": prato,
            "comentarios": prato.comentarios.all(),
        }

        if request.user.tipo_conta == "Cliente":
            return render(request, "models/pedidos/fazer_pedido.html", context)
        elif request.user.tipo_conta == "Garcom":
            return render(request, "models/garcons/fazer_pedido.html", context)
    else:
        msm = "Você precisa estar logado para fazer um pedido!"
    
        return HttpResponseRedirect("/accounts/login/?msm=" + msm)


@login_required
def criar_reserva(request):
    cliente = request.user
    if request.method == "POST":
        msm = ""

        form = ReservaForm(request.POST, cliente_id=cliente.pk)
        if form.is_valid():
            reserva = form.save()
            
            for mesa in reserva.mesa.all():
                reservas = Reserva.objects.filter(mesa=mesa).exclude(id=reserva.pk)

                if reservas:
                    for reserva2 in reservas:
                        if str(reserva.horario) != "00:00:00":
                            if (
                                reserva2.data_reserva == reserva.data_reserva
                                and reserva2.horario == reserva.horario
                            ):
                                msm += f"{mesa} Indisponível para {reserva2.horario} {reserva2.data_reserva}!\n"
                        else:
                            if reserva2.data_reserva == reserva.data_reserva:
                                msm += f"{mesa} Indisponível para {reserva2.data_reserva}!\n"
            if msm == "":
                total = request.POST.get("preco_total")
                return pagar_reserva(request, total)
            
            reserva.delete()
            return redirect("/pedidos/pedir/reserva?msm=" + msm)

    return render(
        request,
        "models/pedidos/fazer_reserva.html",
        {
            "form": ReservaForm(cliente_id=cliente.pk),
            "preco": 20.00,
            "cadeiras_mesa": 4,
        },
    )


def ver_pedido(request, id):
    return render(request, "models/pedidos/ver_pedido.html", {"pedido": Pedido.objects.get(id=id)})

# ================================ CRUD MESA =================================

def gerenciar_mesas(request):
    return render(request, "models/admin_gerente/gerencia_mesas.html", {"mesas": Mesa.objects.all()})
    
    
def criar_editar_mesas(request, id=None):
    mesa = None
    
    if id:
        mesa = Mesa.objects.get(id=id)
        
    if request.method == "POST":
        form = MesaForm(request.POST, instance=mesa)
        
        if form.is_valid():
            form.save()
            return redirect("gerenciar_mesas")
    else:
        form = MesaForm(instance=mesa)
        
    return render(request, "models/forms/form.html", {"form": form, "titulo":"Formulário da Mesa"})


def deletar_mesas(request, id):
    Mesa.objects.get(pk=id).delete()
    return redirect("gerenciar_mesas")