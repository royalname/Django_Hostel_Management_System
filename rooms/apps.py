from django.apps import AppConfig

class RoomsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rooms'

    def ready(self):
        from django.contrib.auth.models import Group
        # Place any code here that needs to run once Django is fully ready
