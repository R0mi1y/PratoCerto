from django.http import JsonResponse
from django.forms.models import model_to_dict
from pedidos.models import *
from pratos.models import *

def atualizar_pedido(request):
    pedidos_restaurante_set = []
    pedidos_site_set = []
    ingredientes_set = []
    receitas_set = []
    
    for pedidoPrato  in PedidoPrato.objects.filter(status='Pendente local'):
        jsonPedidoPrato = model_to_dict(pedidoPrato)
        
        jsonPedidoPrato['prato'] = {
            "nome": pedidoPrato.prato.nome,
            "foto": pedidoPrato.prato.foto.url,
            "descricao": pedidoPrato.prato.descricao,
            "preco": pedidoPrato.prato.preco,
            "id": pedidoPrato.prato.id,
            }
        
        jsonPedidoPrato['pedido'] = model_to_dict(pedidoPrato.pedido)
        
        adicionais = []
        
        for adicional in pedidoPrato.adicional.all():
            adicionais.append({
                        "nome":adicional.nome,
                        "descricao":adicional.descricao,
                        "preco":adicional.preco,
                        "foto":adicional.foto.url,
                    })
        
        jsonPedidoPrato['adicionais'] = adicionais
        
        pedidos_restaurante_set.append(jsonPedidoPrato)
        
        
    for pedidoPrato in PedidoPrato.objects.filter(status='Pendente'):
        jsonPedidoPrato = model_to_dict(pedidoPrato)
        
        jsonPedidoPrato['prato'] = {
            "nome": pedidoPrato.prato.nome,
            "foto": pedidoPrato.prato.foto.url,
            "descricao": pedidoPrato.prato.descricao,
            "preco": pedidoPrato.prato.preco,
            "id": pedidoPrato.prato.id,
            }
        
        jsonPedidoPrato['pedido'] = model_to_dict(pedidoPrato.pedido)
        
        adicionais = []
        
        for adicional in pedidoPrato.adicional.all():
            adicionais.append({
                        "nome":adicional.nome,
                        "descricao":adicional.descricao,
                        "preco":adicional.preco,
                        "foto":adicional.foto.url,
                    })
        
        jsonPedidoPrato['adicionais'] = adicionais
        
        pedidos_site_set.append(jsonPedidoPrato)
        
    for ingrediente in Ingrediente.objects.all():
        ingredientes_set.append(model_to_dict(ingrediente)) 
        
    for receita in Receita.objects.all():
        jsonReceita = model_to_dict(receita)
        ingredientereceitas = []
        
        for ingredientereceita in receita.ingredientereceita_set.all():
            ingredientereceitas.append(model_to_dict(ingredientereceita))
        
        jsonReceita['ingredientereceitas'] = ingredientereceitas
        jsonReceita['prato'] = {
            "nome": receita.prato.nome,
            "foto": receita.prato.foto.url,
            "descricao": receita.prato.descricao,
            "preco": receita.prato.preco,
            "id": receita.prato.id,
        }
        receitas_set.append(jsonReceita)
    
    contexto = {
        'pedidos_restaurante': pedidos_restaurante_set,
        'pedidos_site': pedidos_site_set,
        'ingredientes': ingredientes_set,
        'receitas': receitas_set,
    }
    
    return JsonResponse(contexto)
