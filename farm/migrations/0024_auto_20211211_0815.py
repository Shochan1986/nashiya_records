# Generated by Django 3.2.9 on 2021-12-10 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0023_commentlike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentlike',
            name='users',
        ),
        migrations.AddField(
            model_name='commentlike',
            name='users',
            field=models.CharField(max_length=300, null=True, verbose_name='ユーザー'),
        ),
    ]
