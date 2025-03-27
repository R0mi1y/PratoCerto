from django.urls import path
from .views import settings_view, delete_category

urlpatterns = [
    path("gerenciar/", settings_view, name="settings"),
    path("delete_category/<str:pk>/", delete_category, name="delete_category"),
]
