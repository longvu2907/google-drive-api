from django.apps import AppConfig

class ImageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'image'

    def ready(self):
        from scheduler import updater
        updater.start()
