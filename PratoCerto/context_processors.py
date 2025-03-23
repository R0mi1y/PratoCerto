import re
from PratoCerto import settings


def global_variables(request):
    return {
        'prefix': settings.FORCE_SCRIPT_NAME,
        'APP_NAME': settings.APP_NAME,
        # 'APP_NAME_1': re.findall(r'[A-Z][a-z]*', settings.APP_NAME)[0],
        # 'APP_NAME_2': re.findall(r'[A-Z][a-z]*', settings.APP_NAME)[1] or "",
        # 'APP_ICON': settings.APP_ICON,
    }