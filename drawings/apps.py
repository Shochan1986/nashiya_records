from django.apps import AppConfig


class DrawingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drawings'
    verbose_name = '絵画・工作'
    verbose_name_plural = '絵画・工作'

    def ready(self):
        import drawings.signals

