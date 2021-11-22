from django.apps import AppConfig


class FarmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'farm'
    verbose_name = '農園'
    verbose_name_plural = '農園'

    def ready(self):
        import farm.signals
