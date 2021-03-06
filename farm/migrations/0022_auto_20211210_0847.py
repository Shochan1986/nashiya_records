# Generated by Django 3.2.9 on 2021-12-09 23:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('farm', '0021_images_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='farm.category', verbose_name='分類'),
        ),
        migrations.AlterField(
            model_name='article',
            name='is_public',
            field=models.BooleanField(choices=[(True, '完了済'), (False, '下書中')], default=False, null=True, verbose_name='完成'),
        ),
        migrations.AlterField(
            model_name='article',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='投稿者'),
        ),
    ]
