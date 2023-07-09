from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import *
from django.contrib import messages
from garcons.models import Garcom
from clientes.models import Cliente
from django.contrib.auth.decorators import login_required, permission_required
from rolepermissions.checkers import has_role

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if not request.user.email or request.user.email == "":
            return redirect("cadastrar_cliente")
        else:
            if has_role(request.user, "cliente"):
                return redirect("home_cliente")
            elif has_role(request.user, "garcom"):
                return redirect("home_garcom")
            elif has_role(request.user, "caixa"):
                return redirect("home_caixa")
            elif has_role(request.user, "admin"):
                return redirect("home_admin")
            elif has_role(request.user, "cozinha"):
                return redirect("home_cozinha")    
            else:
                return HttpResponse(request.user.tipo_conta)
    else:
        return redirect("home_cliente")