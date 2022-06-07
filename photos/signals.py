from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    TextSendMessage, 
)
from farm.models import LinePush
from photos.models import Comment, AlbumLike, Reply
from environs import Env 

env = Env() 
env.read_env()  

line_bot_api = LineBotApi(channel_access_token=env("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(channel_secret=env("LINE_CHANNEL_SECRET"))


@receiver(post_save, sender=Comment)
def comment_create_notification(sender, instance, created, **kwargs):
    try:
        if created:
            context = {
                'author': instance.author,
                'image': instance.image,
                'text': instance.text,
            }
            message = render_to_string('photos/comment_message.txt', context)
            for push in LinePush.objects.filter(unfollow=False):
                line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))
    except:
        if created:
            context = {
                'author': instance.author,
                'image': instance.image,
                'text': instance.text,
            }
            subject =  f'コメント＠{instance.image.title}'
            message = render_to_string('photos/comment_message.txt', context)
            from_email = settings.DEFAULT_FROM_EMAIL
            bcc = []
            for user in User.objects.filter(is_staff=True):
                bcc.append(user.email)
            email = EmailMessage(subject, message, from_email, [], bcc)
            email.send()


@receiver(post_save, sender=Reply)
def reply_create_notification(sender, instance, created, **kwargs):
    try:
        if created:
            comment = instance.comment
            writer = instance.comment.author
            album = comment.image
            context = {
                'album' : album,
                'writer' : writer,
                'replier' : instance.author,
                'text' : instance.text,
            }
            message = render_to_string('photos/reply_message.txt', context)
            for push in LinePush.objects.filter(unfollow=False):
                line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))
    except:
        if created:
            comment = instance.comment
            writer = instance.comment.author
            album = comment.image
            context = {
                'album' : album,
                'writer' : writer,
                'replier' : instance.author,
                'text' : instance.text,
            }
            subject =  f'「{instance.author}」さんから「{writer}」さんへの返信　@アルバム「{album}」'
            message = render_to_string('photos/reply_message.txt', context)
            from_email = settings.DEFAULT_FROM_EMAIL
            bcc = []
            for user in User.objects.filter(is_staff=True):
                bcc.append(user.email)
            email = EmailMessage(subject, message, from_email, [], bcc)
            email.send()


@receiver(post_save, sender=AlbumLike)
def album_like_create_notification(sender, instance, created, **kwargs):
    try:
        if created:
            context = {
                'album': instance.album,
                'user': instance.user,
            }
            message = render_to_string('photos/album_like_message.txt', context)
            for push in LinePush.objects.filter(unfollow=False):
                line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))
    except:
        if created:
            context = {
                'album': instance.album,
                'user': instance.user,
            }
            subject =  f'いいね！＠{instance.album.title}'
            message = render_to_string('photos/album_like_message.txt', context)
            from_email = settings.DEFAULT_FROM_EMAIL
            bcc = []
            for user in User.objects.filter(is_staff=True):
                bcc.append(user.email)
            email = EmailMessage(subject, message, from_email, [], bcc)
            email.send()