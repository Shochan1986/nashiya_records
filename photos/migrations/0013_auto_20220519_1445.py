# Generated by Django 3.2.9 on 2022-05-19 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0012_auto_20220518_1947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='content_rt',
        ),
        migrations.AlterField(
            model_name='image',
            name='comment',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='メモ'),
        ),
    ]