from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home, name="home_cliente"),
    path("register", views.criar_usuario_cliente, name="cadastrar_cliente"),
    path('pedidos', views.ver_pedidos, name="ver_pedidos_cliente"),
    path('carrinho', views.ver_carrinho, name="ver carrinho cliente"),
    path('carrinho/remover/<int:id>', views.remover_carrinho, name="remover do carrinho"),
    path('carrinho/editar/<int:id>', views.editar_carrinho, name="editar do carrinho"),
    path('carrinho/comprar', views.comprar_carrinho, name="comprar_carrinho_cliente"),
    path('perfil', views.perfil, name="perfil_cliente"),
    path('perfil/endereco/mudar', views.mudar_endereco, name="trocar endereco padrao"),
    path('endereco/adicionar', views.adicionar_endereco, name="adicionar endereco"),
    path('endereco/deletar/<int:id_endereco>', views.deletar_endereco, name='deletar endereco'),
    path('endereco/editar/<int:id_endereco>', views.editar_endereco, name='editar endereco'),
    path("fazer_pedido/<str:id>", views.fazer_pedido, name="fazer_pedido_cliente"),
    
    path('mudar_foto', views.mudar_foto, name="mudar_foto"),
    path('mudar_foto', views.editar_cliente, name="editar_perfil_cliente"),
    
    path("gerenciar", views.gerenciar_clientes, name='gerenciar_clientes'),
    path("editar/<int:id>", views.editar_cliente, name='editar_cliente'),
    path("deletar/<int:id>", views.deletar_cliente, name='deletar_cliente'),
]