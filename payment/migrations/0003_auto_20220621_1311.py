# Generated by Django 3.2.9 on 2022-06-21 04:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0002_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=300, null=True, verbose_name='名前')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Eメール')),
                ('subject', models.CharField(blank=True, max_length=500, null=True, verbose_name='件名')),
                ('message', models.TextField(blank=True, null=True, verbose_name='メッセージ')),
                ('is_finished', models.BooleanField(default=False, null=True, verbose_name='完了済')),
                ('note', models.CharField(blank=True, max_length=700, null=True, verbose_name='メモ')),
                ('created', models.DateField(auto_now_add=True, null=True, verbose_name='登録日時')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='ブランド'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='分類'),
        ),
        migrations.AlterField(
            model_name='product',
            name='countInStock',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='在庫'),
        ),
        migrations.AlterField(
            model_name='product',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, verbose_name='登録日時'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='詳細'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='商品名'),
        ),
        migrations.AlterField(
            model_name='product',
            name='numReviews',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='レビュー数'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='価格'),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='レート'),
        ),
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='コメント'),
        ),
        migrations.AlterField(
            model_name='review',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, verbose_name='登録日時'),
        ),
        migrations.AlterField(
            model_name='review',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.product', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='レート'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
    ]