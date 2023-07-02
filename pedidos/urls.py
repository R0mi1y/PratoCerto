from django.urls import path
from . import views

urlpatterns = [
    path("pedir/<int:id>", views.fazer_pedido, name="prato"),
    path("pedir/reserva", views.criar_reserva, name="criar reserva")
]