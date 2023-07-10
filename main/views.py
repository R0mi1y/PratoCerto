from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .forms import *
from rolepermissions.checkers import has_role

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if not request.user.email or request.user.email == "":
            return redirect("editar_cliente_cliente")
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
    
def reset_sucess(request):
    msm = "Senha redefinida com sucesso."
    
    return HttpResponseRedirect("/accounts/login/?msm=" + msm)