from django.apps import AppConfig


class PhotosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'photos'
    verbose_name = 'アルバム'
    verbose_name_plural = 'アルバム'

    def ready(self):
        import photos.signals
