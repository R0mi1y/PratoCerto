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


#  ============================ PRATO CRUD ============================  #
@has_role_decorator("admin")
def criar_editar_prato(request, id=None):
    prato = None

    if id:
        prato = Prato.objects.get(id=id)

    if request.method == "POST":
        form = PratoForm(request.POST, request.FILES, instance=prato)

        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = PratoForm(instance=prato)

    return render(request, "models/forms/form.html", {"form": form, "prato": prato})


@has_role_decorator("admin")
def gerenciar_pratos(request):
    pratos = Prato.objects.all()
    return render(
        request,
        "models/admin_gerente/gerencia_pratos.html",
        {"pratos": pratos, "pg": "prato"},
    )


@has_role_decorator("admin")
def deletar_prato(request, id):
    Prato.objects.get(id=id).delete()
    return redirect("gerenciar_prato")




#  ============================ ADICIONAL CRUD ============================  #
@has_role_decorator("admin")
def criar_editar_adicional(request, id=None):
    adicional = None

    if id:
        adicional = Adicional.objects.get(id=id)

    if request.method == "POST":
        form = AdicionalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = AdicionalForm(instance=adicional)
    return render(request, "models/forms/form.html", {"form": form, "adicional":adicional})


@has_role_decorator("admin")
def deletar_adicional(request, id):
    Adicional.objects.get(id=id).delete()
    return redirect("gerenciar_adicionais")





@has_role_decorator("admin")
def gerenciar_adicionais(request):
    context = {
        "adicionais": Adicional.objects.all(),
        "pg": "adicional",
    }

    return render(request, "models/admin_gerente/gerencia_adicionais.html", context)







#  ============================ INGREDIENTE CRUD ============================  #

@has_role_decorator("admin")
def criar_editar_ingrediente(request, id=None):
    ingrediente = None

    if id:
        ingrediente = Ingrediente.objects.get(id=id)

    if request.method == "POST":
        form = IngredienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = IngredienteForm(instance=ingrediente)
    return render(request, "models/forms/form.html", {"form": form, "ingrediente":ingrediente})


@has_role_decorator("admin")
def deletar_ingrediente(request, id):
    Ingrediente.objects.get(id=id).delete()
    return redirect("gerenciar_ingrediente")


@has_role_decorator("admin")
def gerenciar_ingredientes(request):
    context = {
        "ingredientes": Ingrediente.objects.all(),
    }

    return render(request, "models/admin_gerente/gerencia_ingredientes.html", context)


