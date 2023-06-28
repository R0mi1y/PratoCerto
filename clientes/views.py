import hashlib
import random
from django.shortcuts import render, redirect
from django.forms import model_to_dict
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from pedidos.models import Pedido, PedidoPrato
from PratoCerto.settings import AUX
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def home(request):
    if not request.user.email or request.user.email == "":
        return redirect("register")

    cliente = Cliente.objects.get(user=request.user.id)

    data = {}
    data["Categorias"] = AUX["Categorias"]
    data["cliente"] = cliente
    
    if cliente.tipo_conta == "Cliente":
        return render(request, "models/clientes/home.html", data)
    elif cliente.tipo_conta == "Garcom":
        return redirect("home_garcom")


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
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            user = None

        form_user = UserClienteForm(request.POST, prefix="user", instance=user)
        form_cliente = ClienteForm(request.POST, prefix="cliente")

        if form_user.is_valid():
            user = form_user.save(commit=False)
            if not check_password_strength(request.POST.get("user-password")):
                messages.error(
                    request,
                    "A senha deve ter no mínimo 8 caracteres, incluir pelo menos 1 numero, uma letra maiúscula, uma minúscula e um simbolo. Ela não pode ser comum nem similar aos campos do usuário.",
                )

                return redirect("register")

            user.set_password(form_user.cleaned_data["password"])
            user.save()

        if form_cliente.is_valid() and user:
            cliente = form_cliente.save(commit=False)
            cliente.user = user
            try:
                cliente.foto = (
                    SocialAccount.objects.filter(user=user)
                    .first()
                    .extra_data["picture"]
                )
            except:
                pass
            
            cliente.codigo_afiliado = gerar_aleatorio(user.username)
            cliente = cliente.save()
            messages.success(request, "Cadastro realizado com sucesso!")

            return redirect("home")
    else:
        form_user = UserClienteForm(
            prefix="user", instance=User.objects.filter(id=request.user.id).first()
        )
        form_cliente = ClienteForm(prefix="cliente")

    return render(
        request,
        "models/clientes/form.html",
        {"form_user": form_user, "form_cliente": form_cliente},
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

    context = {
        "pedidos": PedidoPrato.objects.filter(cliente=cliente, status="no Carrinho")
    }
    
    return render(request, 'models/clientes/pedidos.html', context)