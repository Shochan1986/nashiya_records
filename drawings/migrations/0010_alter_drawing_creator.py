# Generated by Django 3.2.9 on 2022-05-06 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawings', '0009_drawing_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drawing',
            name='creator',
            field=models.CharField(blank=True, choices=[(1, '仁菜'), (2, '拓海'), (3, '沙織')], default=1, max_length=300, null=True, verbose_name='作者'),
        ),
    ]
