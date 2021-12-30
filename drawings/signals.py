from django.db.models.signals import post_save
from django.dispatch import receiver
from drawings.models import Drawing


@receiver(post_save, sender=Drawing)
def url_one_save(sender, instance, created, **kwargs):
    if instance.image_one and not instance.url_one:
        instance.url_one = instance.image_one.build_url(secure=True)
        instance.save()


@receiver(post_save, sender=Drawing)
def url_two_save(sender, instance, created, **kwargs):
    if instance.image_two and not instance.url_two:
        instance.url_two = instance.image_two.build_url(secure=True)
        instance.save()