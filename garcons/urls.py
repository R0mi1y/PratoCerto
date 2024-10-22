#  =========  GARÇOM  =======  #
from django.urls import path
from . import views
from . import apis

    
urlpatterns = [
    path("home/", views.home, name="home_garcom"),
    path("home/fazer_pedido/<int:id>", views.fazer_pedido, name="fazer_pedido_garcom"),
    path("home/pedidos", views.ver_pedidos, name="ver_pedidos_garcom"),
    path("carrinho", views.ver_carrinho, name="ver_carrinho_garcom"),
    path('carrinho/comprar', views.comprar_carrinho, name="comprar_carrinho_garcom"),
    path('carrinho/editar/<int:id>', views.editar_carrinho, name="editar_carrinho_garcom"),
    path('carrinho/remover/<int:id>', views.remover_carrinho, name="remover_carrinho_garcom"),
    path('servir_pedido/<int:pedido_prato_id>', views.servir_pedido, name='servir_pedido'),
    path('servir_pedido_site/<int:pedido_prato_id>', views.servir_pedido_site, name='servir_pedido_site'),
    path('entregar/<int:pedido_id>', views.entregar, name='entregar'),
    # APIS
    path('get_pedidosPrato/<str:status>', apis.get_pedidoPrato, name='get_pedidosPrato'),
    path('get_pedidos/<str:status>', apis.get_pedidos, name='get_pedidos'),
    # CRUD
    path("cadastrar", views.criar_editar_garcom, name='cadastrar_garcom'),
    path("editar/<int:id>", views.criar_editar_garcom, name='editar_garcom'),
    path("gerenciar", views.gerenciar_garcons, name='gerenciar_garcons'),
    path("deletar/<int:id>", views.deletar_garcom, name='deletar_garcom'),
]