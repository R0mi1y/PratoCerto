import threading
from django.apps import AppConfig

from django.db.utils import OperationalError, ProgrammingError

def ready_callback():
    from .models import get_combined_json
    from PratoCerto import settings as project_settings
    try:
        project_settings.CACHED_CATEGORIES = get_combined_json()
    except (OperationalError, ProgrammingError):
        pass
    

class SettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'settings'

    def ready(self):
        threading.Thread(target=ready_callback).start()
