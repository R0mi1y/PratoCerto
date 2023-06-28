from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("register", views.criar_usuario_cliente, name="register"),
    path('pedidos', views.ver_pedidos, name="ver pedidos"),
    path('carrinho', views.ver_carrinho, name="ver carrinho"),
    path('carrinho/remover/<int:id>', views.remover_carrinho, name="remover do carrinho"),
    path('carrinho/editar/<int:id>', views.editar_carrinho, name="editar do carrinho"),
    path('carrinho/comprar', views.comprar_carrinho, name="comprar carrinho"),
    path('perfil', views.perfil, name="perfil cliente"),
    path('perfil/endereco/mudar', views.mudar_endereco, name="trocar endereco padrao"),
    path('endereco/adicionar', views.adicionar_endereco, name="adicionar endereco"),
    path('endereco/deletar/<int:id_endereco>', views.deletar_endereco, name='deletar endereco'),
    path('endereco/editar/<int:id_endereco>', views.editar_endereco, name='editar endereco'),
]