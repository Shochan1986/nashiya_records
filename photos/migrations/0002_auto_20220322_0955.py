# Generated by Django 3.2.9 on 2022-03-22 00:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='url_one',
        ),
        migrations.RemoveField(
            model_name='image',
            name='url_two',
        ),
    ]
