# views.py
from django.http import HttpResponse
from django.conf import settings

def debug_env(request):
    return HttpResponse(
        f"DEBUG={settings.DEBUG}<br>DB={settings.DATABASES['default']['ENGINE']}"
    )
