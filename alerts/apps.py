import os
from django.apps import AppConfig


class AlertsConfig(AppConfig):
    name = 'alerts'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        #if os.environ.get("RUN_MAIN") != "true":
        #   return
        from .scheduler import start
        start()
