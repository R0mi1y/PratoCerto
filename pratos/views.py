from django.shortcuts import redirect, render
from PratoCerto.settings import AUX
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required


def template_categoria(request, categoria):
    data = {}
    data["pratos"] = Prato.objects.filter(categoria=categoria, disponivel=True)
    
    for tupla in AUX["Categorias"]:
        if tupla[0] == categoria:
            data["Categoria"] = tupla[1]
            break
    
    return render(request, "models/pratos/lista_pratos.html", data)

@login_required
def criar_atualizar_prato(request, prato_id=None):
    prato = None

    if prato_id:
        # Obter a instância existente do prato
        prato = Prato.objects.get(id=prato_id)

    if request.method == 'POST':
        form = PratoForm(request.POST, request.FILES, instance=prato)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PratoForm(instance=prato)

    return render(request, 'models/forms/form.html', {'form': form})


@login_required
def criar_adicional(request):
    if request.method == 'POST':
        form = AdicionalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AdicionalForm()
    return render(request, 'models/forms/form.html', {'form': form})


def template_prato(request, id):
    data = {
        'prato' : Prato.objects.get(id=id)
    }
    
    return render(request, 'models/pratos/prato.html', data)