# Generated by Django 3.2.9 on 2021-12-29 01:54

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drawing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, null=True, verbose_name='タイトル')),
                ('date', models.DateField(blank=True, null=True, verbose_name='作成日')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='コメント')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='登録日時')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日時')),
                ('image_one', cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='画像①')),
                ('image_two', cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='画像②')),
            ],
            options={
                'verbose_name': '作品',
                'verbose_name_plural': '作品',
                'ordering': ['-created'],
            },
        ),
    ]
