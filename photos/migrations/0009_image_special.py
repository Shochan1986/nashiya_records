# Generated by Django 3.2.9 on 2022-05-02 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0008_auto_20220404_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='special',
            field=models.BooleanField(default=False, null=True, verbose_name='特別版'),
        ),
    ]
