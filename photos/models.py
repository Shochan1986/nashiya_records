from django.db import models
from cloudinary.models import CloudinaryField
from mdeditor.fields import MDTextField
from ckeditor_uploader.fields import RichTextUploadingField
from farm.models import LinePush
from linebot.models import (
    TextSendMessage, 
    ImageSendMessage,
    )
from linebot import LineBotApi
from environs import Env 

env = Env() 
env.read_env()


class Image(models.Model):
    title = models.CharField('タイトル' , max_length=300, null=True, )
    date = models.DateField('作成日', null=True, )
    comment = models.CharField('詳細', max_length=500, blank=True, null=True, )
    created = models.DateTimeField('登録日時', auto_now_add=True, null=True, )
    updated = models.DateTimeField('更新日時', auto_now=True, blank=True, null=True, )
    content_rt = RichTextUploadingField(verbose_name='本文(リッチテキスト)', blank=True, null=True, help_text='リッチテキスト形式で書いてください。')
    content = MDTextField(verbose_name='本文(markdown)', blank=True, null=True, help_text='Markdown形式で書いてください。')
    ct_is_public = models.BooleanField('本文を公開する', default=False, null=True)
    special = models.BooleanField('特別版', default=False, null=True)
    image_one = CloudinaryField(
        null=True, 
        verbose_name=('画像①'),
        transformation={ 
            "quality": "auto", 
            'dpr': "auto", 
            "fetch_format":"auto", 
            "angle":"exif", 
            "effect":"auto_contrast",
            "width": 1250, 
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
            "width": 1250, 
            }, 
        )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        verbose_name = '投稿'
        verbose_name_plural = '投稿'

    def line_push(self, request):
        if self.content and self.ct_is_public:
            message = f'になたくアルバム 「{self.title}」 \n URL: https://children-reactjs.netlify.app/photo/{self.id} \n ブログ記事あり！チェック！'
        else:
            message = f'になたくアルバム 「{self.title}」 \n URL: https://children-reactjs.netlify.app/photo/{self.id}'
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
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name='comments', verbose_name="投稿"
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


class ContentImage(models.Model):
    image = models.ForeignKey(Image, on_delete=models.PROTECT)
    content_image = CloudinaryField(
        blank=True, 
        null=True, 
        transformation={
            "quality": "auto:best", 
            'dpr': "auto", 
            "fetch_format":"auto",
            "angle":"exif", 
            "effect":"auto_contrast",
            "width": 1250, 
            }, 
        verbose_name='画像'
        )

    class Meta:
        verbose_name = ('挿入画像')
        verbose_name_plural = ('挿入画像')
