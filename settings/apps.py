import threading
from django.apps import AppConfig

def ready_callback():
    from .models import get_combined_json
    from PratoCerto.settings import CACHED_CATEGORIES
    
    CACHED_CATEGORIES = get_combined_json()
    

class SettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'settings'

    def ready(self):
        threading.Thread(target=ready_callback).start()
