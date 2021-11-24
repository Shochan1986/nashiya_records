# Generated by Django 3.2.9 on 2021-11-24 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0011_auto_20211123_0718'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-date'], 'verbose_name': '日報', 'verbose_name_plural': '日報'},
        ),
        migrations.AddField(
            model_name='images',
            name='comment',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='コメント'),
        ),
        migrations.AlterField(
            model_name='images',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='URL'),
        ),
    ]
