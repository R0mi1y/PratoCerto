from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home_caixa'),
    path('home/pedidos', views.historico_pedidos, name='historico_pedidos'),

        
    path("cadastrar", views.criar_editar_caixa, name='cadastrar_caixa'),
    path("editar/<int:id>", views.criar_editar_caixa, name='editar_caixa'),
    path("gerenciar", views.gerenciar_caixas, name='gerenciar_caixas'),
    path("deletar/<int:id>", views.deletar_caixa, name='deletar_caixa'),
    
]