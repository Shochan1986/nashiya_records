# Generated by Django 3.2.9 on 2022-04-04 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawings', '0007_auto_20220322_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drawing',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='一言'),
        ),
    ]
