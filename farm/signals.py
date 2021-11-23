from django.db.models.signals import post_save
from django.dispatch import receiver

from farm.models import Images

@receiver(post_save, sender=Images)
def images_url_save(sender, instance, created, **kwargs):
    if created:
        if instance.image:
            instance.url = instance.image.url
            instance.save()
