from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    TextSendMessage,
    ImageSendMessage, 
)
from django.core.mail import EmailMultiAlternatives
from farm.models import LinePush
from photos.models import Comment, AlbumLike, ContentImage, Reply, ContentImage
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


@receiver(post_save, sender=ContentImage)
def comment_image_notification(sender, instance, created, **kwargs):
    try:
        if instance.comment:
            context = {
                'album_title': instance.image.title,
                'author': instance.comment.author,
                'text': instance.comment.text,
                'album_id' : instance.image.id,
                'note' : instance.note,
            }
            message = render_to_string('photos/comment_photo.txt', context)
            line_bot_api = LineBotApi(env("LINE_CHANNEL_ACCESS_TOKEN"))
            for push in LinePush.objects.filter(unfollow=False):
                line_bot_api.push_message(
                    push.line_id, 
                    messages=[
                        TextSendMessage(text=message), 
                        ImageSendMessage(
                            original_content_url=instance.content_image.build_url(secure=True), 
                            preview_image_url=instance.content_image.build_url(secure=True)) 
                        ])
    except:
        if instance.comment:
            subject =  f'「写真」@コメント アルバム: {instance.image.title}'
            message = f'「写真」@コメント: {instance.comment.text} <br /> アルバム: {instance.image.title}'
            image_html = f"{message} <br /><br /> \
                リンクはこちら↓ <br /> https://children-reactjs.netlify.app/?redirect=photo/{instance.image.id} <br /><br /> \
                <img src={instance.content_image.build_url(secure=True)} alt={instance.content_image} \
                style='width: 250px; height: 250px;object-fit: cover;border-radius: 5%;' />"
            from_email = settings.DEFAULT_FROM_EMAIL
            bcc = []
            for user in User.objects.filter(is_staff=True):
                bcc.append(user.email)
            email = EmailMultiAlternatives(subject, message, from_email, [], bcc)
            email.attach_alternative(image_html, "text/html")
            email.send()


@receiver(post_save, sender=ContentImage)
def reply_image_notification(sender, instance, created, **kwargs):
    try:
        if instance.reply:
            context = {
                'album_title': instance.image.title,
                'author': instance.reply.author,
                'text': instance.reply.text,
                'album_id' : instance.image.id,
                'note' : instance.note,
            }
            message = render_to_string('photos/reply_photo.txt', context)
            line_bot_api = LineBotApi(env("LINE_CHANNEL_ACCESS_TOKEN"))
            for push in LinePush.objects.filter(unfollow=False):
                line_bot_api.push_message(
                    push.line_id, 
                    messages=[
                        TextSendMessage(text=message), 
                        ImageSendMessage(
                            original_content_url=instance.content_image.build_url(secure=True), 
                            preview_image_url=instance.content_image.build_url(secure=True)) 
                        ])
    except:
        if instance.reply:
            subject =  f'「写真」@返信 アルバム: {instance.image.title}'
            message = f'「写真」@返信: {instance.reply.text} <br /> アルバム: {instance.image.title}'
            image_html = f"{message} <br /><br /> \
                リンクはこちら↓ <br /> https://children-reactjs.netlify.app/?redirect=photo/{instance.image.id} <br /><br /> \
                <img src={instance.content_image.build_url(secure=True)} alt={instance.content_image} \
                style='width: 250px; height: 250px;object-fit: cover;border-radius: 5%;' />"
            from_email = settings.DEFAULT_FROM_EMAIL
            bcc = []
            for user in User.objects.filter(is_staff=True):
                bcc.append(user.email)
            email = EmailMultiAlternatives(subject, message, from_email, [], bcc)
            email.attach_alternative(image_html, "text/html")
            email.send()