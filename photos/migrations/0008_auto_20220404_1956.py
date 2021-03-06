# Generated by Django 3.2.9 on 2022-04-04 10:56

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0007_auto_20220328_2148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['-created'], 'verbose_name': '投稿', 'verbose_name_plural': '投稿'},
        ),
        migrations.AddField(
            model_name='image',
            name='content_rt',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='リッチテキスト形式で書いてください。', null=True, verbose_name='本文(リッチテキスト)'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='photos.image', verbose_name='投稿'),
        ),
        migrations.AlterField(
            model_name='image',
            name='ct_is_public',
            field=models.BooleanField(default=False, null=True, verbose_name='本文を公開する'),
        ),
    ]
