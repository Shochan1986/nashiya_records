from django.template.loader import render_to_string
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    TextSendMessage, 
)
from farm.models import LinePush, Article, Comment, Images
from environs import Env 

env = Env() 
env.read_env()  

line_bot_api = LineBotApi(channel_access_token=env("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(channel_secret=env("LINE_CHANNEL_SECRET"))


@receiver(post_save, sender=Images)
def images_url_save(sender, instance, created, **kwargs):
    if created:
        if instance.image:
            instance.url = instance.image.url
            instance.save()


@receiver(post_save, sender=Article)
def article_create_notification(sender, instance, created, **kwargs):
    if not getattr(instance, 'from_admin_site', False):
        if instance.is_public:
            context = {
                'article': instance,
            }
            message = render_to_string('notify_message.txt', context)
            for push in LinePush.objects.filter(unfollow=False):
                line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))


@receiver(post_save, sender=Comment)
def comment_create_notification(sender, instance, created, **kwargs):
    if created:
        context = {
            'author': instance.author,
            'article': instance.article,
        }
        message = render_to_string('comment_message.txt', context)
        for push in LinePush.objects.filter(unfollow=False):
            line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))


@receiver(post_delete, sender=Comment)
def comment_delete_notification(sender, instance, created, **kwargs):
    if instance.author:
        message = f'「{instance.author}」さんが日報「{instance.article}」へのコメントを削除しました。'
        for push in LinePush.objects.filter(unfollow=False):
            line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))