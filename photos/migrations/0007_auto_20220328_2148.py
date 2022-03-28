# Generated by Django 3.2.9 on 2022-03-28 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0006_alter_image_content'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['-created'], 'verbose_name': '記事', 'verbose_name_plural': '記事'},
        ),
        migrations.AddField(
            model_name='image',
            name='ct_is_public',
            field=models.BooleanField(default=False, null=True, verbose_name='本文公開ステータス'),
        ),
    ]
