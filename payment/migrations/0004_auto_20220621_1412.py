# Generated by Django 3.2.9 on 2022-06-21 05:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0003_auto_20220621_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, verbose_name='登録日'),
        ),
        migrations.AlterField(
            model_name='order',
            name='deliveredAt',
            field=models.DateTimeField(blank=True, null=True, verbose_name='発送日時'),
        ),
        migrations.AlterField(
            model_name='order',
            name='isDelivered',
            field=models.BooleanField(default=False, verbose_name='発送済'),
        ),
        migrations.AlterField(
            model_name='order',
            name='isPaid',
            field=models.BooleanField(default=False, verbose_name='支払済'),
        ),
        migrations.AlterField(
            model_name='order',
            name='paidAt',
            field=models.DateTimeField(blank=True, null=True, verbose_name='支払日時'),
        ),
        migrations.AlterField(
            model_name='order',
            name='paymentMethod',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='支払方法'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shippingPrice',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='送料'),
        ),
        migrations.AlterField(
            model_name='order',
            name='taxPrice',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='税額'),
        ),
        migrations.AlterField(
            model_name='order',
            name='totalPrice',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='合計金額'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='image',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='画像'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='名前'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.order', verbose_name='注文'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='価格'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.product', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='qty',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='数量'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='住所'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='city',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='市町村'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='country',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='都道府県'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.order', verbose_name='注文'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='postalCode',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='郵便番号'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='shippingPrice',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name=''),
        ),
    ]
