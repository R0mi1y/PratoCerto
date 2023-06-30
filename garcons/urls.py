#  =========  GARÇOM  =======  #
from django.urls import path
from . import views

    
urlpatterns = [
    path("home/", views.home, name="home_garcom"),
    path("home/fazer_pedido/<int:id>", views.fazer_pedido, name="fazer_pedido_garcom"),
    path("carrinho", views.ver_carrinho, name="carrinho garcom"),
    path('carrinho/comprar', views.comprar_carrinho, name="comprar carrinho garcom"),
    path('servir_pedido/<int:pedido_prato_id>/', views.servir_pedido, name='servir_pedido'),
]