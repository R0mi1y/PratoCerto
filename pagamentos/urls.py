from django.urls import path
from . import views

urlpatterns = [
    path("pagar", views.process_payment, name="process_payment"),
]