from . import views
from django.urls import path
# from django.http import HttpResponse
# from rolepermissions.roles import assign_role
# from clientes.models import Cliente
# from django.contrib.auth.hashers import make_password

# def criar(request):
#     cliente = Cliente.objects.create(
#         username="admin",
#         email="admin",
#         password=make_password("admin"),
#         tipo_conta="Admin",
#         is_superuser=True,
#     )
#     assign_role(cliente, "admin")
#     return HttpResponse("Criado com sucesso")


urlpatterns = [
    path("", views.home ,name="home"),
    path("reset/sucess", views.reset_sucess ,name="account_reset_password_from_key_done")
    # path("teste", criar)
]