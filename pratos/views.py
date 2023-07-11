from django.shortcuts import redirect, render
from clientes.models import Cliente
from PratoCerto.settings import AUX
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator


def template_categoria(request, categoria):
    data = {}
    data["pratos"] = Prato.objects.filter(categoria=categoria, disponivel=True)
    
    for tupla in AUX["Categorias"]:
        if tupla[0] == categoria:
            data["Categoria"] = tupla[1]
            break
    data['cliente'] = request.user
    
    return render(request, "models/pratos/lista_pratos.html", data)


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

        if form.is_valid() :
            prato = form.save(commit=False)  # Salvar o prato sem enviar ao banco de dados ainda
            
            prato.save()
            for id in request.POST.getlist("adicional"):
                adicional = Adicional.objects.get(id=id)
                prato.adicional.add(adicional)
            prato.save()
            
            if request.POST.get('receita'):
                receita = Receita.objects.get(id=request.POST.get('receita'))
                receita.prato = prato
                receita.save()

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
        form = AdicionalForm(request.POST, request.FILES, instance=adicional)
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
        form = IngredienteForm(request.POST, request.FILES, instance=ingrediente)
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


@has_role_decorator("admin")
def gerenciar_estoque(request):

    ingredientes = Ingrediente.objects.all()
    return render(request, 'models/admin_gerente/estoque.html', {'ingredientes': ingredientes})


@has_role_decorator("admin")
def atualizar_quantidade(request, ingrediente_id):
    ingrediente = Ingrediente.objects.get(id=ingrediente_id)
    if request.method == 'POST':
        quantidade = int(request.POST['quantidade'])
        ingrediente.quantidade_estoque = quantidade
        ingrediente.save()
    return redirect('gerenciar_estoque')


# ============ CRUD RECEITAS =========== #
@has_role_decorator("admin")
def gerenciar_receitas(request):
    pass


def editar_receita(request, id): 
    pass


def deletar_receita(request, id): 
    pass
    
    
def criar_receita(request):    
    if request.method == "POST":
        receita = Receita.objects.create(nome=request.POST.get('nome_receita'))
        
        for item_name in request.POST:
            if 'item_' in item_name:
                item_id = item_name.replace('item_','')
                
                IngredienteReceita.objects.create(
                    ingrediente=Ingrediente.objects.get(pk=item_id),
                    receita=receita,
                    quantidade=float(request.POST.get('quantidade_' + item_id))
                )
        
        return redirect('home_admin')
    else:
        ingredientes = Ingrediente.objects.all()
    return render(request, "models/pratos/prato_receita_form.html", {"ingredientes":ingredientes})