from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("register", views.criar_usuario_cliente, name="register"),
    path('pedidos', views.ver_pedidos, name="ver pedidos"),
    path('carrinho', views.ver_carrinho, name="ver carrinho"),
]