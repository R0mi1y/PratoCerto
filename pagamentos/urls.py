from django.urls import path
from . import views

urlpatterns = [
    path("sucesso", views.retorno_mercadopago, name="sucess_payment"),
]