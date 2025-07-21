from django.apps import AppConfig


class PointSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'point_system'
    def ready(self):
        import  point_system.signals # makes sure receivers are registered
