# Generated by Django 3.2.9 on 2021-11-22 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0009_auto_20211123_0529'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='album',
        ),
        migrations.RemoveField(
            model_name='images',
            name='album',
        ),
        migrations.RemoveField(
            model_name='images',
            name='default',
        ),
        migrations.DeleteModel(
            name='ImageAlbum',
        ),
    ]
