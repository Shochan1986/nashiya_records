# Generated by Django 3.2.9 on 2021-12-01 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0019_delete_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='更新日時'),
        ),
    ]