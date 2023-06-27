from django.urls import path
from . import views

urlpatterns = [
    path("categoria/<str:categoria>", views.template_categoria, name="lista_pratos"),
    path("cadastro/prato", views.criar_atualizar_prato, name="Cadastro_prato"),
    path("cadastro/adicional", views.criar_adicional, name="Cadastro_prato"),
    path("comentar/<int:id_prato>", views.comentar, name="fazer comentario"),
    path("comentar/<int:id_prato>/<int:id_comentario>", views.responder_comentario, name="responder comentario"),
]