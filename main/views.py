from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import *
from django.contrib import messages
from garcons.models import Garcom
from clientes.models import Cliente
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if not request.user.email or request.user.email == "":
            return redirect("cadastrar_cliente")
        else:
            if request.user.tipo_conta == "Cliente":
                return redirect("home_cliente")
            elif request.user.tipo_conta == "Garcom":
                return redirect("home_garcom")
            elif request.user.tipo_conta == "Caixa":
                return redirect("home_caixa")
            elif request.user.tipo_conta == "Admin":
                return redirect("home_admin")
            elif request.user.tipo_conta == "Cozinha":
                return redirect("home_cozinha")    
            else:
                return HttpResponse(request.user.tipo_conta)
    else:
        return redirect("home_cliente")