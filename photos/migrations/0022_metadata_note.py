# Generated by Django 3.2.9 on 2022-06-04 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0021_alter_image_cimg_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='metadata',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='メモ'),
        ),
    ]