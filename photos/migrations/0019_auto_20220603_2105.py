# Generated by Django 3.2.9 on 2022-06-03 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0018_metadata'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='metadata',
            options={'ordering': ['-created'], 'verbose_name': 'メタデータ', 'verbose_name_plural': 'メタデータ'},
        ),
        migrations.AddField(
            model_name='metadata',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='登録日時'),
        ),
        migrations.AddField(
            model_name='metadata',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='更新日時'),
        ),
    ]