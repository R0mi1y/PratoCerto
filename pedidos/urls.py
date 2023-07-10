from django.urls import path
from . import views

urlpatterns = [
    path("pedir/<int:id>", views.fazer_pedido, name="prato"),
    path("pedir/reserva", views.criar_reserva, name="criar reserva"),
    path("ver/<int:id>", views.ver_pedido, name="ver_pedido"),
    
    path('mesa/gerenciar', views.gerenciar_mesas, name="gerenciar_mesas"),
    path('mesa/cadastrar', views.criar_editar_mesas, name="cadastrar_mesa"),
    path('mesa/editar/<int:id>', views.criar_editar_mesas, name="editar_mesa"),
    path('mesa/deletar/<int:id>', views.deletar_mesas, name="deletar_mesa"),
]