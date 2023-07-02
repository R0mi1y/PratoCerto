from django.shortcuts import render, redirect
from clientes.models import Cliente
from .forms import *
from pratos.models import Prato, Comentario
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def fazer_pedido(request, id):
    cliente = request.user
    prato = Prato.objects.get(id=id)

    if request.method == "POST":
        pedidoPrato_form = PedidoPratoForm(request.POST, prato_id=id)

        if pedidoPrato_form.is_valid():
            pedidoPrato = pedidoPrato_form.save(commit=False)
            pedidoPrato.cliente = cliente
            pedidoPrato.nome_cliente = cliente.username
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
                                msm += f"{mesa} indisponível para {reserva2.horario} {reserva2.data_reserva}!\n"
                        else:
                            if reserva2.data_reserva == reserva.data_reserva:
                                msm += f"{mesa} indisponível para {reserva2.data_reserva}!\n"
            if msm == "":
                return redirect("home")
            reserva.delete()
            messages.error(request, msm)

    return render(
        request,
        "models/pedidos/fazer_reserva.html",
        {
            "form": ReservaForm(cliente_id=cliente.pk),
            "preco": 20.00,
            "cadeiras_mesa": 4,
        },
    )
