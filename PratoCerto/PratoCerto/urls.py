from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('caixa/', include('checkout.urls')),
    path('cozinha/', include('kitchen.urls')),
    path('garcom/', include('waiter.urls')),
    path('cliente/', include('client.urls')),
]
