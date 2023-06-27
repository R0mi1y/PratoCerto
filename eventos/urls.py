from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home_eventos"),
    path("home/create/", views.criar_evento, name="criar_evento"),
    path("home/delete/<int:evento_id>/", views.deletar_evento, name="deletar_evento"),
    path("home/edit/<int:evento_id>/", views.editar_evento, name="editar_evento"),
]
