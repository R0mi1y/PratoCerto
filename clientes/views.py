import hashlib
import random
from django.shortcuts import get_object_or_404, render, redirect
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from pedidos.forms import PedidoPratoForm, PedidoForm, GarcomPedidoForm
from pedidos.models import Pedido, PedidoPrato
from PratoCerto.settings import AUX
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password


@login_required
def home(request):
    if not request.user.email or request.user.email == "":
        return redirect("register")

    data = {}
    data["Categorias"] = AUX["Categorias"]
    data["cliente"] = request.user
    
    if request.user.tipo_conta == "Cliente":
        return render(request, "models/clientes/home.html", data)
    elif request.user.tipo_conta == "Garcom":
        return redirect("home_garcom")
    elif request.user.tipo_conta == "Cozinha":
        return redirect("home_cozinha")


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
            cliente.save()
            
            return redirect("home")
        except Cliente.DoesNotExist:
            if form_cliente.is_valid():
                cliente = form_cliente.save(commit=False)
                        
                if not cliente.pontos:
                    cliente.pontos = 0
                try:
                    cliente.foto = (
                        SocialAccount.objects.filter(user=request.user)
                        .first()
                        .extra_data["picture"]
                    )
                except:
                    pass
                
                cliente.codigo_afiliado = gerar_aleatorio(cliente.username)
                cliente = cliente.save()
                messages.success(request, "Cadastro realizado com sucesso!")

                return redirect("home")
    else:
        form_cliente = ClienteForm(instance=Cliente.objects.filter(pk=request.user.pk).first())

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


@login_required
def ver_pedidos(request):
    cliente = Cliente.objects.get(user=request.user.id)

    context = {
        "pedidos": Pedido.objects.filter(cliente=cliente).exclude(status="no Carrinho")
    }
    
    return render(request, 'models/clientes/pedidos.html', context)


@login_required
def ver_carrinho(request):
    cliente = Cliente.objects.get(user=request.user.id)
    if cliente.tipo_conta == "Garcom":
        return redirect("carrinho garcom")

    context = {
        "pedidos": PedidoPrato.objects.filter(cliente=cliente, status="no Carrinho")
    }
    
    return render(request, 'models/clientes/carrinho.html', context)


@login_required
def remover_carrinho(request, id):
    PedidoPrato.objects.get(id=id).delete()
    return redirect("ver carrinho")


@login_required
def editar_carrinho(request, id):
    cliente = Cliente.objects.get(user_id=request.user.pk)
    pedidoPrato = PedidoPrato.objects.get(id=id)
    
    if request.method == "POST":
        form = PedidoPratoForm(request.POST, prato_id=pedidoPrato.prato.pk, instance=pedidoPrato)
        if form.is_valid():
            pedidoPrato = form.save(commit=False)
            pedidoPrato.cliente = cliente
            pedidoPrato.save()
            
            return redirect("ver carrinho")
        
    context = {
        'prato_form' : PedidoPratoForm(instance=pedidoPrato, prato_id=pedidoPrato.prato.pk),
        'prato'      : pedidoPrato.prato,
        'comentarios': pedidoPrato.prato.comentarios.all(),
    }
    return render(request, 'models/pedidos/fazer_pedido.html', context)


@login_required
def comprar_carrinho(request):
    cliente = Cliente.objects.get(user=request.user.id)
    pedidosPrato = PedidoPrato.objects.filter(cliente=cliente, status="no Carrinho")
    
    if cliente.tipo_conta == "Garcom":
        return redirect("comprar carrinho garcom")
    
    if request.method == "POST":
        if cliente.tipo_conta == "Cliente":
            form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cliente = cliente
            total = 0
            
            for pedidoPrato in pedidosPrato:
                total += pedidoPrato.prato.preco * pedidoPrato.quantidade
                pedidoPrato.status = "Pendente"
                pedidoPrato.pedido = pedido
                
            pedido.total = total
            pedido.save()
            
            [pedidoPrato.save() for pedidoPrato in pedidosPrato]
            
            return redirect("ver pedidos")

    context = {
        "pedidos": pedidosPrato,
        "form": PedidoForm(cliente_id=cliente.pk),
    }
    
    return render(request, 'models/pedidos/pagamento.html', context)


@login_required
def adicionar_endereco(request):
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.cliente = Cliente.objects.get(username=request.user.username)
            endereco.save()
            
            return redirect('perfil cliente')
    else:
        form = EnderecoForm()
    
    return render(request, 'models/clientes/add_endereco.html', {'form': form})


@login_required
def mudar_endereco(request):
    cliente = Cliente.objects.get(user=request.user.id)
    enderecos = Endereco.objects.filter(cliente=cliente)
    
    if request.method == 'POST':
        id = request.POST.get('id_endereco')
        endereco = Endereco.objects.get(id=id)
        endereco.padrao = True
        endereco.save()
        
        return redirect('perfil cliente')

    contexto = {
        'cliente': cliente,
        'enderecos': enderecos
    }
    
    return render(request, 'models/clientes/mudar_endereco.html', contexto)
    

@login_required
def perfil(request):
    cliente = Cliente.objects.get(username=request.user.username)
    try:
        endereco = Endereco.objects.get(cliente=cliente, padrao=True)
    except Endereco.DoesNotExist:
        return redirect('adicionar endereco')
    
    contexto = {
        'cliente': cliente,
        'endereco': endereco,
    }        
     
    return render(request, 'models/clientes/perfil.html', contexto)


@login_required
def deletar_endereco(request, id_endereco):
    endereco = get_object_or_404(Endereco, pk=id_endereco)
    
    endereco.delete()
    return redirect('trocar endereco padrao')


@login_required
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

