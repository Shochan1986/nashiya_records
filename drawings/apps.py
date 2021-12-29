from django.apps import AppConfig


class DrawingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drawings'
    verbose_name = '絵画'
    verbose_name_plural = '絵画'

    def ready(self):
        import drawings.signals

