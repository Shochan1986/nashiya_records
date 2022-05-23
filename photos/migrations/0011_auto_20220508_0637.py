# Generated by Django 3.2.9 on 2022-05-07 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0010_auto_20220507_0609'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=300, null=True, verbose_name='ユーザー')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='作成日時')),
                ('album', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='photos.image', verbose_name='アルバム')),
            ],
            options={
                'verbose_name': 'いいね(アルバム)',
                'verbose_name_plural': 'いいね(アルバム)',
                'ordering': ['-created'],
            },
        ),
        migrations.DeleteModel(
            name='CommentLike',
        ),
    ]