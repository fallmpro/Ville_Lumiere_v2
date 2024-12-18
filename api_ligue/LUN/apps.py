from django.apps import AppConfig


class LunConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LUN'

def ready(self):
        import LUN.signals