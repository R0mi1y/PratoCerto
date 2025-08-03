from django.contrib import admin
from .models import Pedido, Adicional, Mesa, Reserva, PedidoPrato

admin.site.register(Pedido)
admin.site.register(Adicional)
admin.site.register(Mesa)
admin.site.register(Reserva)
admin.site.register(PedidoPrato)