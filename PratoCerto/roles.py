from rolepermissions.roles import AbstractUserRole

class Cliente(AbstractUserRole):
    available_permissions = {
        "fazer_pedido_cliente": True,
        "home_cliente": True,
        
    }
    
class Garcom(AbstractUserRole):
    available_permissions = {
        "fazer_pedido_garcom": True,
        "home_garcom": True,
    }
    
class Cozinha(AbstractUserRole):
    available_permissions = {
        "home_cozinha": True,
    }    

class Caixa(AbstractUserRole):
    avaliable_permissions = {
        "home_caixa": True,
    }
    
class Admin(AbstractUserRole):
    avaliable_permissions = {
        "home_cozinha": True,
        "home_caixa": True,
        "fazer_pedido_garcom": True,
        "home_garcom": True,
        "fazer_pedido_cliente": True,
        "home_cliente": True,
    }