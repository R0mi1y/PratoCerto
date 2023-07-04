from django.shortcuts import redirect, render
from clientes.models import Cliente
from PratoCerto.settings import AUX
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator


@login_required
def template_categoria(request, categoria):
    data = {}
    data["pratos"] = Prato.objects.filter(categoria=categoria, disponivel=True)
    
    for tupla in AUX["Categorias"]:
        if tupla[0] == categoria:
            data["Categoria"] = tupla[1]
            break
    data['cliente'] = request.user
    
    return render(request, "models/pratos/lista_pratos.html", data)


@login_required
def template_prato(request, id):
    data = {
        'prato' : Prato.objects.get(id=id)
    }
    
    return render(request, 'models/pratos/prato.html', data)


@login_required
def comentar(request, id_prato):
    if request.method == 'POST':
        prato = Prato.objects.get(id=id_prato)
        texto = request.POST.get("comentario")
        comentario = Comentario.objects.create(
            texto=texto,
            cliente=request.user
        )
        
        prato.comentarios.add(comentario.pk)
        prato.save()
    
    return redirect("/clientes/fazer_pedido/" + str(id_prato))


@login_required
def responder_comentario(request, id_prato, id_comentario):
    if request.method == 'POST':
        comentario = Comentario.objects.get(id=id_comentario)
        resposta = Comentario.objects.create(
            texto=request.POST.get("comentario"),
            cliente=request.user
        )
        
        comentario.respostas.add(resposta)
    
    return redirect("/clientes/fazer_pedido/" + str(id_prato))
