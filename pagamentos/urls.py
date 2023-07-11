from django.urls import path
from . import views

urlpatterns = [
    path("pagar", views.pagar_pedido, name="process_payment"),
    path("pagar1", views.teste1),
]