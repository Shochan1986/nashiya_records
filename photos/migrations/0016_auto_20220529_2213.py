# Generated by Django 3.2.9 on 2022-05-29 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0015_auto_20220525_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentimage',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='content_images', to='photos.image', verbose_name='アルバム'),
        ),
        migrations.AlterField(
            model_name='image',
            name='cimg_is_public',
            field=models.BooleanField(default=False, null=True, verbose_name='ギャラリーの公開'),
        ),
        migrations.AlterField(
            model_name='image',
            name='ct_is_public',
            field=models.BooleanField(default=False, null=True, verbose_name='本文の公開'),
        ),
        migrations.AlterField(
            model_name='image',
            name='special',
            field=models.BooleanField(default=False, null=True, verbose_name='父ちゃん日記'),
        ),
    ]
