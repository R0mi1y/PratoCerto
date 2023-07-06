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


@login_required
def home(request):
    # print(get_user_roles(request.user))

    data = {}
    data["Categorias"] = AUX["Categorias"]
    data["cliente"] = request.user
    
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
            cliente = Cliente.objects.get(username=request.POST.get("username"))
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
                messages.error(request, "Imagem não salva")
            cliente.save()
        except Cliente.DoesNotExist:
            if form_cliente.is_valid():
                cliente = form_cliente.save(commit=False)

                if not cliente.pontos:
                    cliente.pontos = 0

                cliente.tipo_conta = "Cliente"
                cliente.codigo_afiliado = gerar_aleatorio(cliente.username)
                cliente.save()
                messages.success(request, "Cadastro realizado com sucesso!")

        assign_role(cliente, "cliente")

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
    
    return redirect("ver_carrinho_cliente")


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
        if cliente.tipo_conta == "Cliente":
            form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
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
                
            pedido.total = total
            pedido.save()
            
            [pedidoPrato.save() for pedidoPrato in pedidosPrato]
            
            return redirect("ver_pedidos_cliente")

    context = {
        "pedidos": pedidosPrato,
        "form": PedidoForm(cliente_id=cliente.pk),
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
    
    return render(request, 'models/forms/form.html', {'form': form})


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

    return render(request, 'models/clientes/add_endereco.html', {'form': form})


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

