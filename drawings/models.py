from django.db import models
from cloudinary.models import CloudinaryField

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
            "effect":"auto_contrast" 
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
            "effect":"auto_contrast" 
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
