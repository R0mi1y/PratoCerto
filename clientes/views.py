import hashlib
import random
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from PratoCerto import settings
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from pratos.models import *
from pedidos.forms import PedidoPratoForm, PedidoForm, GarcomPedidoForm
from pedidos.models import *
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import make_password
from rolepermissions.roles import assign_role, get_user_roles
from rolepermissions.decorators import has_permission_decorator, has_permission, has_role_decorator
from django.utils import timezone
from eventos.models import Evento
from pagamentos.views import pagar_pedido
from main.models import Referencia

def home(request):
    current_datetime = timezone.now()
    id_pratos = Referencia.objects.filter(chave="recomendacoes")
    
    recomendados = []
    
    [recomendados.append(Prato.objects.get(id=i.valor)) for i in id_pratos]
    
    data = {
        "Categorias":AUX["Categorias"],
        "cliente": request.user,
        "eventos": Evento.objects.filter(data_inicio__lte=current_datetime, data_termino__gte=current_datetime),
        "recomendados":recomendados,
        "notificacao": True,
    }
    
    return render(request, "models/clientes/home.html", data)


def check_password_strength(password):
    try:
        validate_password(password)
        # A senha atende aos requisitos
        return True
    except ValidationError as e:
        # A senha não atende aos requisitos
        return False


def criar_usuario_cliente(request):
    if request.method == "POST":
        form_cliente = ClienteForm(request.POST)

        try:
            print("Recuperando usuario...")
            cliente = Cliente.objects.get(username=request.POST.get("username"))
            print("Usuario Recuperado!")
            cliente.password = make_password(request.POST.get("password"))
            cliente.cpf = request.POST.get('cpf')
            cliente.telefone = request.POST.get('telefone')
            cliente.email = request.POST.get('email')
            cliente.tipo_conta = "Cliente"
            cliente.codigo_afiliado = gerar_aleatorio(cliente.username)
            try:
                cliente.foto = (
                    SocialAccount.objects.filter(user=request.user)
                    .first()
                    .extra_data["picture"]
                )
            except:
                cliente.foto = "/media/system/default_perfil.png"
            cliente.save()
            assign_role(cliente, "cliente")
        except Cliente.DoesNotExist:
            print("Usuario não encontrado, realizando cadastro!")
            if form_cliente.is_valid():
                cliente = form_cliente.save(commit=False)

                if not cliente.pontos:
                    cliente.pontos = 0

                cliente.tipo_conta = "Cliente"
                cliente.codigo_afiliado = gerar_aleatorio(cliente.username)
                cliente.foto = "/media/system/default_perfil.png"
                cliente.save()
                assign_role(cliente, "cliente")
                messages.success(request, "Cadastro realizado com sucesso!")

            return redirect("home")
    else:
        form_cliente = ClienteForm(instance=Cliente.objects.filter(username=request.user.username).first())

    return render(
        request,
        "models/clientes/registrar.html",
        {"form_cliente": form_cliente},
    )


def gerar_aleatorio(string):
    # Concatena a string com um valor aleatório (neste caso, um número inteiro)
    string_aleatoria = string + str(random.randint(1, 10000))
    
    # Aplica a função de hash (SHA-256) à string aleatória
    hash_object = hashlib.sha256(string_aleatoria.encode())
    hash_hex = hash_object.hexdigest()
    
    print(hash_hex)
    
    return (hash_hex[:2] + string + hash_hex[2:4]).upper()


@has_role_decorator("cliente")
def ver_pedidos(request):
    cliente = request.user

    context = {
        "pedidos": Pedido.objects.filter(cliente=cliente).exclude(status="no Carrinho")
    }
    
    return render(request, 'models/clientes/pedidos.html', context)


@has_role_decorator("cliente")
def ver_carrinho(request):
    cliente = request.user

    context = {
        "pedidos": PedidoPrato.objects.filter(cliente=cliente, status="no Carrinho")
    }
    
    return render(request, 'models/clientes/carrinho.html', context)


@login_required
def remover_carrinho(request, id):
    cliente = request.user
    pedido = get_object_or_404(PedidoPrato, id=id, cliente=cliente)
    pedido.delete()
    
    return redirect("ver carrinho cliente")


@login_required
def editar_carrinho(request, id):
    cliente = request.user
    pedidoPrato = PedidoPrato.objects.get(cliente=request.user ,id=id)
    
    if request.method == "POST":
        form = PedidoPratoForm(request.POST, prato_id=pedidoPrato.prato.pk, instance=pedidoPrato)
        if form.is_valid():
            pedidoPrato = form.save(commit=False)
            pedidoPrato.cliente = cliente
            pedidoPrato.save()
            
            return redirect("ver_carrinho_cliente")
        
    context = {
        'prato_form' : PedidoPratoForm(instance=pedidoPrato, prato_id=pedidoPrato.prato.pk),
        'prato'      : pedidoPrato.prato,
        'comentarios': pedidoPrato.prato.comentarios.all(),
    }
    return render(request, 'models/pedidos/fazer_pedido.html', context)


@has_role_decorator("cliente")
def comprar_carrinho(request):
    cliente = request.user
    pedidosPrato = PedidoPrato.objects.filter(cliente=cliente, status="no Carrinho")
    
    if request.method == "POST":
        if request.POST.get('endereco') != 'null':
            pedido = Pedido(
                metodo_pagamento=request.POST.get('metodo_pagamento'),
                endereco=Endereco.objects.filter(pk=request.POST.get('endereco')).first(),
                local_retirada=request.POST.get('local_retirada')
                )
        else:
            pedido = Pedido(
                metodo_pagamento=request.POST.get('metodo_pagamento'),
                local_retirada=request.POST.get('local_retirada')
                )
        
        pedido.cliente = cliente
        total = 0
        if pedido.local_retirada == "entrega":
            pedido.taxa_entrega = settings.AUX["frete_entrega"]
            total += pedido.taxa_entrega
        else:
            pedido.taxa_entrega = 0
            
        for pedidoPrato in pedidosPrato:
            total += pedidoPrato.prato.preco * pedidoPrato.quantidade
            pedidoPrato.status = "Pendente"
            pedidoPrato.pedido = pedido
            
        cliente.pontos = float(total) / float(settings.AUX['pontos']['por_valor_compra'])
        valor_preco_pontos = None
        if request.POST.get('usar_pontos'):
            total = float(total) - float(settings.AUX['pontos']['valor_rs']) * float(cliente.pontos)
            valor_preco_pontos = float(total) - float(settings.AUX['pontos']['valor_rs']) * float(cliente.pontos)
            cliente.pontos = 0
        
        pedido.status = "Pendente"
        pedido.total = total
        
        pedido.save()
        [pedidoPrato.save() for pedidoPrato in pedidosPrato]
        
        cliente.save()
        
        if pedido.local_retirada == 'entrega' and pedido.metodo_pagamento != 'dinheiro':
            return pagar_pedido(request, pedido, valor_preco_pontos)
        return redirect("home_cliente")
    total = 0
                
    for pedidoPrato in pedidosPrato:
        total += pedidoPrato.prato.preco * pedidoPrato.quantidade
    
    context = {
        "pedidos": pedidosPrato,
        "form": PedidoForm(cliente_id=cliente.pk),
        "total": total,
        "taxa_entrega": settings.AUX["frete_entrega"],
        'valor_rs': settings.AUX['pontos']['valor_rs'],
    }
    
    return render(request, 'models/pedidos/pagamento.html', context)


@has_role_decorator("cliente")
def adicionar_endereco(request):
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.cliente = Cliente.objects.get(username=request.user.username)
            endereco.save()
            
            return redirect('perfil_cliente')
    else:
        form = EnderecoForm()
    
    return render(request, 'models/forms/form.html', {'form': form, "titulo":"Cadastro de Endereço"})


@has_role_decorator("cliente")
def mudar_endereco(request):
    cliente = request.user
    enderecos = Endereco.objects.filter(cliente=cliente)
    
    if request.method == 'POST':
        id = request.POST.get('id_endereco')
        endereco = Endereco.objects.get(id=id)
        endereco.padrao = True
        endereco.save()
        
        return redirect('perfil_cliente')

    contexto = {
        'cliente': cliente,
        'enderecos': enderecos
    }
    
    return render(request, 'models/clientes/mudar_endereco.html', contexto)
    

@has_role_decorator("cliente")
def perfil(request):
    cliente = request.user
    try:
        endereco = Endereco.objects.get(cliente=cliente, padrao=True)
    except Endereco.DoesNotExist:
        return redirect('adicionar endereco')
    
    contexto = {
        'cliente': cliente,
        'endereco': endereco,
    }        
     
    return render(request, 'models/clientes/perfil.html', contexto)


@has_role_decorator("cliente")
def deletar_endereco(request, id_endereco):
    endereco = get_object_or_404(Endereco, pk=id_endereco)
    
    endereco.delete()
    return redirect('trocar endereco padrao')


@has_role_decorator("cliente")
def editar_endereco(request, id_endereco):
    endereco = get_object_or_404(Endereco, pk=id_endereco)

    if request.method == 'POST':
        form = EditarEnderecoForm(request.POST, instance=endereco)
        if form.is_valid():
            form.save()
            return redirect('trocar endereco padrao')
    else:
        form = EditarEnderecoForm(instance=endereco)

    return render(request, 'models/forms/form.html', {'form': form, "titulo":"Editar Endereço"})


@has_role_decorator("cliente")
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
            
            for id in request.POST.getlist("adicional"):
                adicional = Adicional.objects.get(pk=id)
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

    return render(request, "models/pedidos/fazer_pedido.html", context)


@login_required
def mudar_foto(request):
    if request.method == "POST":
        cliente = request.user
        cliente.foto = request.FILE.get("foto")
        cliente.save()
        
    return redirect("perfil_cliente")


#  ============================ CLIENTE CRUD ============================  #
@has_role_decorator("admin")
def editar_cliente(request, id):
    cliente = None
    
    if id:
        cliente = Cliente.objects.get(id=id)
    
    if request.method == "POST":
        form = EditarClienteFormAdmin(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()

            return redirect("gerenciar_clientes")
    else:
        form = EditarClienteFormAdmin(instance=cliente)
    return render(request, "models/forms/form.html", {"form": form, "cliente": cliente, "titulo":"Editar Cliente"})


@login_required
def editar_cliente_cliente(request):
    cliente = request.user
    
    if request.method == "POST":
        form = ClienteFormEditar(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            assign_role(cliente, "cliente")
            user = authenticate(request, username=cliente.username, password=cliente.password)

            if user is not None:
                # Realizar o login do cliente autenticado
                login(request, user)
                
                return redirect("adicionar endereco")
            else:
                # Tratar caso as credenciais sejam inválidas
                return redirect('account_login')  # Redirecionar para a página de login novamente
                
    else:
        form = ClienteFormEditar(instance=cliente)
    return render(request, "models/forms/form.html", {"form": form, "cliente": cliente, "titulo":"Editar Cliente"})


@has_role_decorator("admin")
def deletar_cliente(request, id):
    Cliente.objects.get(id=id).delete()
    return redirect("gerenciar_clientes")


@has_role_decorator("admin")
def gerenciar_clientes(request):
    return render(
        request,
        "models/admin_gerente/gerencia.html",
        {"clientes": Cliente.objects.filter(tipo_conta="Cliente"), "pg": "cliente"},
    )
