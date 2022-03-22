# Generated by Django 3.2.9 on 2022-03-22 01:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0002_auto_20220322_0955'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200, null=True, verbose_name='投稿者')),
                ('text', models.TextField(null=True, verbose_name='本文')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='作成日時')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新日時')),
            ],
            options={
                'verbose_name': 'コメント',
                'verbose_name_plural': 'コメント',
                'ordering': ['-created'],
            },
        ),
        migrations.AlterField(
            model_name='image',
            name='comment',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='詳細'),
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=300, null=True, verbose_name='ユーザー')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='作成日時')),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='photos.comment', verbose_name='コメント')),
            ],
            options={
                'verbose_name': 'いいね(コメント)',
                'verbose_name_plural': 'いいね(コメント)',
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='drawing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='photos.image', verbose_name='作品'),
        ),
    ]
