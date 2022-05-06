from calendar import c
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
    
    class CreatorChoices(models.TextChoices):
        NINA = 1, ('仁菜')
        TAKUMI = 2, ('拓海') 
        SAORI = 3, ('沙織')
        SHOTARO = 4, ('祥太朗')

    title = models.CharField('タイトル' , max_length=300, null=True, )
    date = models.DateField('作成日', null=True, )
    description = models.CharField('メモ', max_length=500, blank=True, null=True, )
    created = models.DateTimeField('登録日時', auto_now_add=True, null=True, )
    updated = models.DateTimeField('更新日時', auto_now=True, blank=True, null=True, )
    creator = models.CharField('作者', max_length=300, null=True, choices=CreatorChoices.choices, default=CreatorChoices.NINA)
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

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        verbose_name = '作品'
        verbose_name_plural = '作品'

    def line_push(self, request):
        message = f'Nina作 「{self.title}」 \n URL: https://daughter-blog-berraquera.vercel.app/{self.id}'
        line_bot_api = LineBotApi(env("LINE_CHANNEL_ACCESS_TOKEN"))
        # if not self.image_two:
        for push in LinePush.objects.filter(unfollow=False):
            line_bot_api.push_message(
                push.line_id, 
                messages=[
                    TextSendMessage(text=message), 
                    ImageSendMessage(
                        original_content_url=self.image_one.build_url(secure=True), 
                        preview_image_url=self.image_one.build_url(secure=True))
                    ])
        # else:
        #     for push in LinePush.objects.filter(unfollow=False):
        #         line_bot_api.push_message(
        #             push.line_id, 
        #             messages=[
        #                 TextSendMessage(text=message), 
        #                 ImageSendMessage(
        #                     original_content_url=self.image_one.build_url(secure=True), 
        #                     preview_image_url=self.image_one.build_url(secure=True)),
        #                 ImageSendMessage(
        #                     original_content_url=self.image_two.build_url(secure=True), 
        #                     preview_image_url=self.image_two.build_url(secure=True)),
        #                 ])


class Comment(models.Model):
    drawing = models.ForeignKey(
        Drawing, on_delete=models.CASCADE, related_name='comments', verbose_name="作品"
    )
    author = models.CharField(max_length=200, verbose_name=('投稿者'), null=True)
    text = models.TextField(verbose_name=('本文'), null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=('作成日時'), null=True)
    updated = models.DateTimeField('更新日時', auto_now=True, blank=True, null=True, )

    class Meta:
        ordering = ['-created']
        verbose_name = ('コメント')
        verbose_name_plural = ('コメント')

    def __str__(self):
        return self.text


class CommentLike(models.Model):
    user = models.CharField('ユーザー', null=True, max_length=300, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, related_name='likes', verbose_name='コメント')
    created = models.DateTimeField(auto_now_add=True, verbose_name=('作成日時'), null=True)

    class Meta:
        ordering = ['-created']
        verbose_name = ('いいね(コメント)')
        verbose_name_plural = ('いいね(コメント)')

    def __str__(self):
        return self.comment.text + f'({self.comment.author})' + ' by ' + self.user
