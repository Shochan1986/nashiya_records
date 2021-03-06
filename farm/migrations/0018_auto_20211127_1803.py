# Generated by Django 3.2.9 on 2021-11-27 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('farm', '0017_auto_20211127_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200, null=True, verbose_name='投稿者')),
                ('text', models.TextField(null=True, verbose_name='本文')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='作成日時')),
            ],
            options={
                'verbose_name': 'コメント',
                'verbose_name_plural': 'コメント',
                'ordering': ['-created'],
            },
        ),
        migrations.AlterField(
            model_name='article',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='投稿者'),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200, null=True, verbose_name='投稿者')),
                ('text', models.TextField(null=True, verbose_name='本文')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='作成日時')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='farm.comment', verbose_name='返信')),
            ],
            options={
                'verbose_name': '返信',
                'verbose_name_plural': '返信',
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='farm.article', verbose_name='日報'),
        ),
    ]
