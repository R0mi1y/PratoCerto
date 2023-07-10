from django.urls import path
from . import views
from . import apis

urlpatterns = [
    # outras URLs do seu projeto...
    path('home/', views.home, name='home_cozinha'),
    path('home/pedido/pronto/<int:pedido_id>/', views.pedido_pronto, name='pedido_pronto'),
    
    path("cadastrar", views.criar_editar_cozinha, name='cadastrar_cozinha'),
    path("editar/<int:id>", views.criar_editar_cozinha, name='editar_cozinha'),
    path("gerenciar", views.gerenciar_cozinhas, name='gerenciar_cozinhas'),
    path("deletar/<int:id>", views.deletar_cozinha, name='deletar_cozinha'),
    
    path('atualizar_pedido', apis.atualizar_pedido, name='atualizar_pedido'),
]
