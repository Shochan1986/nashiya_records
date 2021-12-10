from django.db import models
#from django.utils import timezone
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Pears(models.Model):
    name = models.CharField('品種', null=True, max_length=200)
    created = models.DateTimeField('追加日', auto_now_add=True, null=True)
    number = models.PositiveIntegerField('番号', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['number']
        verbose_name = '品種'
        verbose_name_plural = '品種'


class Images(models.Model):
    url = models.URLField('URL', blank=True, null=True)
    image = CloudinaryField(
        null=True, 
        verbose_name=('画像ファイル'),
         transformation={ 
            "quality": "auto", 
            'dpr': "auto", 
            "fetch_format":"auto", 
            "angle":"exif", 
            "effect":"auto_contrast" 
            }, 
        )
    author = models.CharField(max_length=200, verbose_name=('投稿者'), null=True, blank=True)
    comment = models.TextField('コメント', blank=True, null=True)
    created = models.DateTimeField('追加日', auto_now_add=True, null=True)

    def __str__(self):
        return str(self.image.url)

    class Meta:
        ordering = ['-created']
        verbose_name = '写真'
        verbose_name_plural = '写真'


class Fields(models.Model):
    name = models.CharField('名前', null=True, max_length=300)
    place = models.CharField('場所', null=True, max_length=400)
    number = models.PositiveIntegerField('番号', null=True, blank=True)
    created = models.DateTimeField('追加日', auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['number']
        verbose_name = '作業場所'
        verbose_name_plural = '作業場所'


class Category(models.Model):
    name = models.CharField('名前', null=True, max_length=300)
    number = models.PositiveIntegerField('番号', null=True, blank=True)
    created = models.DateTimeField('追加日', auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['number']
        verbose_name = '分類'
        verbose_name_plural = '分類'


class Article(models.Model):

    PUBLISHED_CHOICES = ((True, '完了済'), (False, '下書中'))

    user = models.ForeignKey(User, models.SET_NULL, null=True, verbose_name='投稿者', related_name='articles')
    category = models.ForeignKey(Category, models.SET_NULL, null=True, verbose_name='分類', related_name='articles')
    title = models.CharField('作業内容' ,max_length=300, null=True, )
    fields = models.ManyToManyField(Fields, blank=True, verbose_name='作業場所', related_name='articles')
    date = models.DateField('日付', blank=True, null=True, )
    description = models.TextField('詳細', blank=True, null=True, )
    start_time = models.DateTimeField('開始時間', blank=True, null=True, )
    end_time = models.DateTimeField('終了時間', blank=True, null=True, )
    created = models.DateTimeField('作成日時', auto_now_add=True, null=True, )
    updated = models.DateTimeField('更新日時', auto_now=True, blank=True, null=True, )
    is_public = models.BooleanField('完成', default=False, null=True, choices=PUBLISHED_CHOICES, )
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='完成日時')
    images = models.ManyToManyField(Images, blank=True, verbose_name='画像', related_name='articles')
    pears = models.ManyToManyField(Pears, blank=True, verbose_name='品種', related_name='articles')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        verbose_name = '日報'
        verbose_name_plural = '日報'

    # def save(self, *args, **kwargs):
    #     if self.is_public and not self.published_at:
    #         self.published_at = timezone.now()
    #     super().save(*args, **kwargs)


class LinePush(models.Model):
    line_id = models.CharField(max_length=50, primary_key=True, verbose_name="LineID", default="0")
    line_name = models.CharField(max_length=100, verbose_name="Line表示名", null=True)
    line_picture_url = models.URLField(verbose_name="Line画像URL", null=True)
    line_status_message = models.CharField(max_length=100, blank=True, null=True, verbose_name="Lineメッセージ")
    unfollow = models.BooleanField(default=False, verbose_name="ブロック", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")

    def __str__(self):
        return self.line_id
    
    class Meta:
        verbose_name = ('LINE登録')
        verbose_name_plural = ('LINE登録')
        ordering = ['-create_time']


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments', verbose_name="日報"
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
    users = models.ManyToManyField(User, blank=True, verbose_name='ユーザー')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, related_name='likes', verbose_name='いいね')
    created = models.DateTimeField(auto_now_add=True, verbose_name=('作成日時'), null=True)

    class Meta:
        ordering = ['-created']
        verbose_name = ('いいね(コメント)')
        verbose_name_plural = ('いいね(コメント)')

    def __str__(self):
        return str(self.comment.likes.count())
