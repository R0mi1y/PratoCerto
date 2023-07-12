from django.shortcuts import redirect, render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Evento
from .forms import EventoForm
from rolepermissions.decorators import has_role_decorator

def home(request):
    events = Evento.objects.all()  
    
    if events:
        return render(request, 'models/eventos/eventos.html', {'events': events, 'user': request.user})
    else:
        return render(request, 'models/eventos/eventos.html', {'user': request.user})


@has_role_decorator("admin")
def criar_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home_eventos')
    else:
        form = EventoForm()
    
    context = {'form': form, 
               "titulo":"Cadastro de Eventos"
               }
    return render(request, 'models/forms/form.html', context)


@has_role_decorator("garcom")
def deletar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    if request.method == 'POST':
        evento.delete()
        return redirect('home_eventos')
    
    return render(request, 'models/eventos/deletar_eventos.html', {'evento': evento})


@has_role_decorator("garcom")
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('home_eventos')
    else:
        form = EventoForm(instance=evento)
    
    return render(request, 'models/forms/form.html', {'form': form, 'evento': evento, "titulo":"Cadastro de Eventos", "titulo":"Editar Evento"})
