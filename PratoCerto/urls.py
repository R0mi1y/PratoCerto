from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_django/', admin.site.urls),
    path('cozinhas/', include('cozinhas.urls')),
    path('caixas/', include('caixas.urls')),
    path('clientes/', include('clientes.urls')),
    path('garcons/', include('garcons.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('pratos/', include('pratos.urls')),
    path('eventos/', include('eventos.urls')),
    path('accounts/', include('allauth.urls')),
    path('pagamentos/', include('pagamentos.urls')),
    path('admin/', include('admin_gerente.urls')),
    path('', include('main.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
