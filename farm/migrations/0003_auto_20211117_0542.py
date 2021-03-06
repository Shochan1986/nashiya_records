# Generated by Django 3.2.9 on 2021-11-16 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0002_auto_20211116_0805'),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.ImageField(null=True, upload_to='', verbose_name='名前')),
                ('place', models.ImageField(null=True, upload_to='', verbose_name='場所')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='追加日')),
            ],
            options={
                'verbose_name': '畑',
                'verbose_name_plural': '畑',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='', verbose_name='画像ファイル')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='追加日')),
            ],
            options={
                'verbose_name': '写真',
                'verbose_name_plural': '写真',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Pears',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='品種')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='追加日')),
            ],
            options={
                'verbose_name': '品種',
                'verbose_name_plural': '品種',
                'ordering': ['-created'],
            },
        ),
        migrations.RemoveField(
            model_name='article',
            name='image1',
        ),
        migrations.RemoveField(
            model_name='article',
            name='image2',
        ),
        migrations.AlterField(
            model_name='article',
            name='is_public',
            field=models.BooleanField(default=False, null=True, verbose_name='完成'),
        ),
        migrations.AddField(
            model_name='article',
            name='images',
            field=models.ManyToManyField(blank=True, to='farm.Images', verbose_name='画像'),
        ),
        migrations.AddField(
            model_name='article',
            name='pears',
            field=models.ManyToManyField(blank=True, to='farm.Pears', verbose_name='品種'),
        ),
        migrations.AlterField(
            model_name='article',
            name='field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='farm.field', verbose_name='畑'),
        ),
    ]
