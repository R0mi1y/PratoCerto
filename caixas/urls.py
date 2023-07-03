from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home_caixa'),
    path('home/pedidos', views.historico_pedidos, name='historico_pedidos'),
]