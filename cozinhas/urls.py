from django.urls import path
from . import views
from .views import home, pedido_pronto

urlpatterns = [
    # outras URLs do seu projeto...
    path('home/', views.home, name='home_cozinha'),
    path('home/pedido/pronto/<int:pedido_id>/', views.pedido_pronto, name='pedido_pronto'),
]
