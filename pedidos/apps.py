from django.apps import AppConfig


class PedidoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pedidos'

    def ready(self):
        import pedidos.cron

