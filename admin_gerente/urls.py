from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home, name="home_admin"),
    path("criar_superuser", views.criar_editar_admin, name="create_superuser"),
    path("editar_superuser/<int:id>", views.criar_editar_admin, name="create_superuser"),
    
    path("recomendacoes", views.ver_recomendacoes, name="gerenciar_recomendacoes"),
    path("recomendacoes/deletar/<int:id>", views.deletar_recomendacao, name="deletar_recomendacoes"),
    path("recomendacoes/adicionar/<int:id>", views.add_recomendacao, name="adicionar_recomendacoes"),
]
