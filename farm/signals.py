from django.template.loader import render_to_string
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    TextSendMessage, 
    ImageSendMessage,
)
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from farm.models import LinePush, Article, Comment, Images, CommentLike, ArticleLike
from django.utils import timezone
from django.utils.timezone import localtime 
from environs import Env 

env = Env() 
env.read_env()  

line_bot_api = LineBotApi(channel_access_token=env("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(channel_secret=env("LINE_CHANNEL_SECRET"))


def updateUser(sender, instance, **kwargs):
    user = instance
    if user.email != '':
        user.username = user.email
pre_save.connect(updateUser ,sender=User)


@receiver(post_save, sender=Images)
def images_url_save(sender, instance, created, **kwargs):
    if created:
        if instance.image:
            instance.url = instance.image.build_url(secure=True)
            instance.save()


@receiver(post_save, sender=User)
def user_registered_notification(sender, instance, created, **kwargs):
    try:
        if created:
            message = f'「{instance.first_name}」さんのアカウントが登録されました。'
            for push in LinePush.objects.filter(unfollow=False):
                line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))
    except:
        pass


# @receiver(post_save, sender=User)
# def user_admin_registered_notification(sender, instance, created, **kwargs):
#     try:
#         if instance.is_staff:
#             message = f'「{instance.first_name}」さんのアカウントが承認されました。'
#             for push in LinePush.objects.filter(unfollow=False):
#                 line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))
#     except:
#         pass


@receiver(post_delete, sender=User)
def user_deleted_notification(sender, instance, **kwargs):
    try:
        message = f'「{instance.first_name}」さんのアカウントが削除されました。'
        for push in LinePush.objects.filter(unfollow=False):
            line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))
    except:
        pass


@receiver(post_save, sender=Article)
def article_published_notification(sender, instance, created, **kwargs):
    try:
        if not getattr(instance, 'from_admin_site', False):
            if instance.is_public and not instance.published_at:
                instance.published_at = localtime(timezone.now())
                instance.save()
                context = {
                    'article': instance,
                }
                message = render_to_string('notify_message.txt', context)
                for push in LinePush.objects.filter(unfollow=False):
                    line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))
                    if instance.images:
                        for photo in instance.images.all():
                            line_bot_api.push_message(push.line_id, messages=ImageSendMessage(
                                original_content_url=photo.url,
                                preview_image_url=photo.url,
                            ))
    except:
        pass
           

@receiver(post_save, sender=Comment)
def comment_create_notification(sender, instance, created, **kwargs):
    try:
        if not getattr(instance, 'from_admin_site', False):
            if created:
                context = {
                    'author': instance.author,
                    'article': instance.article,
                    'text': instance.text,
                }
                message = render_to_string('comment_message.txt', context)
                for push in LinePush.objects.filter(unfollow=False):
                    line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))
    except:
        pass


@receiver(post_save, sender=CommentLike)
def comment_like_create_notification(sender, instance, created, **kwargs):
    try:
        if not getattr(instance, 'from_admin_site', False):
            if created:
                context = {
                    'comment': instance.comment,
                    'article': instance.comment.article,
                    'user': instance.user,
                }
                message = render_to_string('comment_like_message.txt', context)
                for push in LinePush.objects.filter(unfollow=False):
                    line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))
    except:
        pass


@receiver(post_save, sender=ArticleLike)
def article_like_create_notification(sender, instance, created, **kwargs):
    try:
        if not getattr(instance, 'from_admin_site', False):
            if created:
                context = {
                    'article': instance.article,
                    'user': instance.user,
                }
                message = render_to_string('article_like_message.txt', context)
                for push in LinePush.objects.filter(unfollow=False):
                    line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))
    except:
        pass

