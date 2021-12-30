from django.db import models
from cloudinary.models import CloudinaryField
from farm.models import LinePush
from django.template.loader import render_to_string
from linebot.models import (
    TextSendMessage, 
    ImageSendMessage,
    )
from linebot import LineBotApi
from environs import Env 

env = Env() 
env.read_env()


class Drawing(models.Model):
    title = models.CharField('タイトル' , max_length=300, null=True, )
    date = models.DateField('作成日', null=True, )
    comment = models.CharField('コメント', max_length=500, blank=True, null=True, )
    created = models.DateTimeField('登録日時', auto_now_add=True, null=True, )
    updated = models.DateTimeField('更新日時', auto_now=True, blank=True, null=True, )
    image_one = CloudinaryField(
        null=True, 
        verbose_name=('画像①'),
        transformation={ 
            "quality": "auto", 
            'dpr': "auto", 
            "fetch_format":"auto", 
            "angle":"exif", 
            "effect":"auto_contrast",
            }, 
        )
    image_two = CloudinaryField(
        null=True, 
        blank=True,
        verbose_name=('画像②'),
         transformation={ 
            "quality": "auto", 
            'dpr': "auto", 
            "fetch_format":"auto", 
            "angle":"exif", 
            "effect":"auto_contrast",
            }, 
        )
    url_one = models.URLField('URL①', blank=True, null=True)
    url_two = models.URLField('URL②', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        verbose_name = '作品'
        verbose_name_plural = '作品'

    def line_push(self, request):
        message = f'Nina作 「{self.title}」 \n URL: https://daughter-blog-berraquera.vercel.app/{self.id}'
        line_bot_api = LineBotApi(env("LINE_CHANNEL_ACCESS_TOKEN"))
        for push in LinePush.objects.filter(unfollow=False):
            line_bot_api.push_message(
                push.line_id, 
                messages=[
                    TextSendMessage(text=message), 
                    ImageSendMessage(
                        original_content_url=self.url_one, 
                        preview_image_url=self.url_one)
                    ])
