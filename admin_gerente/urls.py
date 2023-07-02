from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home, name="home_admin"),
    path("create_superuser", views.criar_editar_admin, name="create_superuser"),
    
    path("Cliente/gerenciar", views.gerenciar_clientes, name='gerenciar_clientes'),
    path("Cliente/editar/<int:id>", views.editar_cliente, name='editar_cliente'),
    path("Cliente/deletar/<int:id>", views.deletar_cliente, name='deletar_cliente'),
    
    path("Prato/cadastrar", views.criar_editar_prato, name='cadastrar_prato'),
    path("Prato/editar/<int:id>", views.criar_editar_prato, name='editar_prato'),
    path("Prato/gerenciar", views.gerenciar_pratos, name='gerenciar_prato'),
    path("Prato/deletar/<int:id>", views.deletar_prato, name='deletar_prato'),
    
    path("Caixa/cadastrar", views.criar_editar_caixa, name='cadastrar_caixa'),
    path("Caixa/editar/<int:id>", views.criar_editar_caixa, name='editar_caixa'),
    path("Caixa/gerenciar", views.gerenciar_caixas, name='gerenciar_caixas'),
    path("Caixa/deletar/<int:id>", views.deletar_caixa, name='deletar_caixa'),
    
    path("Cozinha/cadastrar", views.criar_editar_cozinha, name='cadastrar_cozinha'),
    path("Cozinha/editar/<int:id>", views.criar_editar_cozinha, name='editar_cozinha'),
    path("Cozinha/gerenciar", views.gerenciar_cozinhas, name='gerenciar_cozinhas'),
    path("Cozinha/deletar/<int:id>", views.deletar_cozinha, name='deletar_cozinha'),
    
    path("Garcom/cadastrar", views.criar_editar_garcom, name='cadastrar_garcom'),
    path("Garcom/editar/<int:id>", views.criar_editar_garcom, name='editar_garcom'),
    path("Garcom/gerenciar", views.gerenciar_garcons, name='gerenciar_garcons'),
    path("Garcom/deletar/<int:id>", views.deletar_garcom, name='deletar_garcom'),
    
    path("Adicional/cadastrar", views.criar_editar_adicional, name='cadastrar_adicional'),
    path("Adicional/editar/<int:id>", views.criar_editar_adicional, name='editar_adicional'),
    path("Adicional/gerenciar", views.gerenciar_adicionais, name='gerenciar_adicionais'),
    path("Adicional/deletar/<int:id>", views.deletar_adicional, name='deletar_adicional'),
]
