from django.urls import path
from . import views

urlpatterns = [
    path("fazer_pedido/<str:prato>", views.fazer_pedido, name="fazer pedido"),
    path("pedir/<int:id>", views.fazer_pedido, name="prato"),
]