# Generated by Django 3.2.9 on 2021-12-31 16:07

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, null=True, verbose_name='タイトル')),
                ('date', models.DateField(null=True, verbose_name='作成日')),
                ('comment', models.CharField(blank=True, max_length=500, null=True, verbose_name='コメント')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='登録日時')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日時')),
                ('image_one', cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='画像①')),
                ('image_two', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='画像②')),
                ('url_one', models.URLField(blank=True, null=True, verbose_name='URL①')),
                ('url_two', models.URLField(blank=True, null=True, verbose_name='URL②')),
            ],
            options={
                'verbose_name': '写真',
                'verbose_name_plural': '写真',
                'ordering': ['-created'],
            },
        ),
    ]
