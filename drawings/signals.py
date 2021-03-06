from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    TextSendMessage, 
)
from farm.models import LinePush
from drawings.models import Comment
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
                'drawing': instance.drawing,
                'text': instance.text,
            }
            message = render_to_string('drawings/comment_message.txt', context)
            for push in LinePush.objects.filter(unfollow=False):
                line_bot_api.push_message(push.line_id, messages=TextSendMessage(text=message))
    except:
        pass