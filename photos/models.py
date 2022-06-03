from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
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


class Tags(models.Model):
    name = models.CharField('名称', null=True, max_length=200)
    created = models.DateTimeField('追加日', auto_now_add=True, null=True)
    number = models.PositiveIntegerField('番号', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['number']
        verbose_name = 'タグ'
        verbose_name_plural = 'タグ'


class Image(models.Model):
    title = models.CharField('タイトル' , max_length=300, null=True, )
    date = models.DateField('日付', null=True, )
    comment = models.CharField('メモ', max_length=500, blank=True, null=True, )
    created = models.DateTimeField('登録日時', auto_now_add=True, null=True, )
    updated = models.DateTimeField('更新日時', auto_now=True, blank=True, null=True, )
    content_rt = RichTextUploadingField(verbose_name='本文(リッチテキスト)', blank=True, null=True, help_text='リッチテキスト形式で書いてください。')
    content = MDTextField(verbose_name='本文(markdown)', blank=True, null=True, help_text='Markdown形式で書いてください。')
    ct_is_public = models.BooleanField('本文の公開', default=False, null=True)
    cimg_is_public = models.BooleanField('ギャラリーの公開', default=False, null=True)
    special = models.BooleanField('父ちゃん日記', default=False, null=True)
    tags = models.ManyToManyField(Tags, blank=True, verbose_name='タグ', related_name='images')
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
        ordering = ['-date']
        verbose_name = '投稿'
        verbose_name_plural = '投稿'

    def line_push(self, request):
        if self.content and self.ct_is_public:
            message = f'になたくアルバム 「{self.title}」 \n URL: https://children-reactjs.netlify.app/photo/{self.id} \n ブログ記事あり！チェック！'
        else:
            message = f'になたくアルバム 「{self.title}」 \n URL: https://children-reactjs.netlify.app/photo/{self.id}'
        line_bot_api = LineBotApi(env("LINE_CHANNEL_ACCESS_TOKEN"))
        for push in LinePush.objects.filter(unfollow=False):
            line_bot_api.push_message(
                push.line_id, 
                messages=[
                    TextSendMessage(text=message), 
                    ImageSendMessage(
                        original_content_url=self.image_one.build_url(secure=True), 
                        preview_image_url=self.image_one.build_url(secure=True)) 
                    ])

    def email_push(self, request):
        subject = f'「{self.title}」| になたくアルバム'
        message = f'「{self.title}」'
        image_html = f"リンクはこちら↓ <br /> https://children-reactjs.netlify.app/?redirect=photo/{self.id} <br /><br /> \
            <img src={self.image_one.build_url(secure=True)} alt={self.title} \
            style='width: 250px; height: 250px;object-fit: cover;border-radius: 5%;' />"
        from_email = settings.DEFAULT_FROM_EMAIL
        bcc = []
        for user in User.objects.filter(is_staff=True):
            bcc.append(user.email)
        email = EmailMultiAlternatives(subject, message, from_email, [], bcc)
        email.attach_alternative(image_html, "text/html")
        email.send()


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


class AlbumLike(models.Model):
    user = models.CharField('ユーザー', null=True, max_length=300, blank=True)
    album = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, related_name='likes', verbose_name='アルバム')
    created = models.DateTimeField(auto_now_add=True, verbose_name=('作成日時'), null=True)

    class Meta:
        ordering = ['-created']
        verbose_name = ('いいね(アルバム)')
        verbose_name_plural = ('いいね(アルバム)')

    def __str__(self):
        return self.album.title + ' by ' + self.user


class ContentImage(models.Model):
    image = models.ForeignKey(
        Image, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='content_images',
        verbose_name='アルバム'
    )
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

    def __str__(self):
        if self.image:
            return str(self.id) + ' ' + f'[{self.image.title}]'
        else:
            return str(self.id)


class Metadata(models.Model):
    album = models.ForeignKey(Image, verbose_name='アルバム', related_name='metadata', null=True, blank=True, on_delete=models.SET_NULL)
    site_url = models.URLField('サイトURL', null=True)
    site_name = models.CharField('サイト名', null=True, blank=True, max_length=500)
    title = models.CharField('タイトル', null=True, blank=True, max_length=500)
    image_url = models.URLField('画像URL', null=True, blank=True)
    description = models.TextField('詳細', null=True, blank=True)
    created = models.DateTimeField('登録日時', auto_now_add=True, null=True, )
    updated = models.DateTimeField('更新日時', auto_now=True, blank=True, null=True, )

    class Meta:
        ordering = ['-created']
        verbose_name = ('メタデータ')
        verbose_name_plural = ('メタデータ')

    def __str__(self):
        if self.title:
            return self.title
        else:
            return 'メタデータ'