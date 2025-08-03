from django.contrib import admin
from .models import Prato, Ingrediente, Comentario, Receita, IngredienteReceita

admin.site.register(Prato)
admin.site.register(Ingrediente)
admin.site.register(Comentario)
admin.site.register(Receita)
admin.site.register(IngredienteReceita)