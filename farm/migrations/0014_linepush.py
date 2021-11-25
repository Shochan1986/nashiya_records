# Generated by Django 3.2.9 on 2021-11-25 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0013_alter_images_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinePush',
            fields=[
                ('line_id', models.CharField(default='0', max_length=50, primary_key=True, serialize=False, verbose_name='LineID')),
                ('line_name', models.CharField(max_length=100, null=True, verbose_name='Line表示名')),
                ('line_picture_url', models.URLField(null=True, verbose_name='Line画像URL')),
                ('line_status_message', models.CharField(blank=True, max_length=100, null=True, verbose_name='Lineメッセージ')),
                ('unfollow', models.BooleanField(default=False, null=True, verbose_name='ブロック')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='登録日時')),
            ],
            options={
                'verbose_name': 'LINE登録者リスト',
                'verbose_name_plural': 'LINE登録者リスト',
                'ordering': ['-create_time'],
            },
        ),
    ]
