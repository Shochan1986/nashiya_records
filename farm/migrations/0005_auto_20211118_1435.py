# Generated by Django 3.2.9 on 2021-11-18 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0004_auto_20211118_1220'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='field',
            options={'ordering': ['name'], 'verbose_name': '作業場', 'verbose_name_plural': '作業場'},
        ),
        migrations.AlterField(
            model_name='field',
            name='name',
            field=models.CharField(max_length=300, null=True, verbose_name='名前'),
        ),
        migrations.AlterField(
            model_name='field',
            name='place',
            field=models.CharField(max_length=400, null=True, verbose_name='場所'),
        ),
    ]
