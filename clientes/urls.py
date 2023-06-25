from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("register", views.criar_usuario_cliente, name="register"),
]