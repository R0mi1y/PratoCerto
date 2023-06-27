from django.shortcuts import redirect, render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Evento
from .forms import EventoForm


def home(request):
    # Sua lógica para recuperar eventos e informações do usuário
    events = Evento.objects.all()  # Exemplo de recuperação de eventos usando um modelo Event

    if events:
        # Renderize o template com eventos e informações do usuário
        return render(request, 'models/eventos/eventos.html', {'events': events, 'user': request.user})
    else:
        # Renderize o template sem eventos e informações do usuário
        return render(request, 'models/eventos/eventos.html', {'user': request.user})

def criar_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_eventos')
    else:
        form = EventoForm()
    
    context = {'form': form}
    return render(request, 'models/eventos/criar_eventos.html', context)


def deletar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    if request.method == 'POST':
        evento.delete()
        return redirect('home_eventos')
    
    return render(request, 'models/eventos/deletar_eventos.html', {'evento': evento})


def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('home_eventos')
    else:
        form = EventoForm(instance=evento)
    
    return render(request, 'models/eventos/editar_eventos.html', {'form': form, 'evento': evento})
