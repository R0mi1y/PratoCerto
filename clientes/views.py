from django.shortcuts import render, redirect
from django.forms import model_to_dict
from django.http import JsonResponse
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from PratoCerto.settings import AUX
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


@login_required
def home(request):
    if not request.user.email or request.user.email == "":
        return redirect("register")

    user2 = model_to_dict(request.user)
    clienteTrue = Cliente.objects.get(user=request.user.id)
    userTrue = model_to_dict(clienteTrue.user)
    clienteTrue = model_to_dict(clienteTrue)

    data = {"msm": [user2, userTrue, clienteTrue]}
    data["Categorias"] = AUX["Categorias"]

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
