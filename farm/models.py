from django.db import models

class Article(models.Model):
    title = models.CharField('タイトル' ,max_length=300, null=True, )
    field = models.CharField('畑', max_length=300, blank=True, null=True, )
    task = models.CharField('内容', max_length=300, blank=True, null=True, )
    description = models.TextField('詳細', blank=True, null=True, )
    start_time = models.DateTimeField('開始時間', blank=True, null=True, )
    end_time = models.DateTimeField('終了時間', blank=True, null=True, )
    created = models.DateTimeField('作成日時', auto_now_add=True, blank=True, null=True, )
    updated = models.DateTimeField('更新日時', auto_now=True, blank=True, null=True, )
    is_public = models.BooleanField('完成', default=False, blank=True, null=True, )
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='完成日時')
    image1 = models.ImageField('画像①', blank=True, null=True)
    image2 = models.ImageField('画像②', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        verbose_name = '日報'
        verbose_name_plural = '日報'
