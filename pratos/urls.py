from django.urls import path
from . import views

urlpatterns = [
    path("categoria/<str:categoria>", views.template_categoria, name="lista_pratos"),
    path("comentar/<int:id_prato>", views.comentar, name="fazer comentario"),
    path("comentar/<int:id_prato>/<int:id_comentario>", views.responder_comentario, name="responder comentario"),
    
    # CRUD PRATOS
    path("cadastrar", views.criar_editar_prato, name='cadastrar_prato'),
    path("editar/<int:id>", views.criar_editar_prato, name='editar_prato'),
    path("gerenciar", views.gerenciar_pratos, name='gerenciar_prato'),
    path("deletar/<int:id>", views.deletar_prato, name='deletar_prato'),

    # CRUD ADICIONAL
    path("Adicional/cadastrar", views.criar_editar_adicional, name='cadastrar_adicional'),
    path("Adicional/editar/<int:id>", views.criar_editar_adicional, name='editar_adicional'),
    path("Adicional/gerenciar", views.gerenciar_adicionais, name='gerenciar_adicionais'),
    path("Adicional/deletar/<int:id>", views.deletar_adicional, name='deletar_adicional'),

    # CRUD INGREDIENTES

    path("Ingrediente/cadastrar", views.criar_editar_ingrediente, name='cadastrar_ingrediente'),
    path("Ingrediente/editar/<int:id>", views.criar_editar_ingrediente, name='editar_ingrediente'),    
    path("Ingrediente/deletar/<int:id>", views.deletar_ingrediente, name='deletar_ingrediente'),

    # GERENCIA DE ESTOQUE 

    path("Estoque/gerenciar", views.gerenciar_estoque, name="gerenciar_estoque"),
    path("Estoque/Atualizar_quantidade/<int:ingrediente_id>", views.atualizar_quantidade, name="atualizar_quantidade"),


    # Receita
    path("receitas/cadastrar", views.criar_receita, name="cadastrar_receita"),
    path("receitas/editar/<int:id>", views.editar_receita, name="editar_receita"),
    path("receitas/deletar/<int:id>", views.deletar_receita, name="deletar_receita"),
    
]