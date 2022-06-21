from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='ユーザー')
    name = models.CharField('商品名', max_length=200, null=True, blank=True)
    image = CloudinaryField(
        blank=True, 
        null=True, 
        transformation={
            "quality": "auto:best", 
            'dpr': "auto", 
            "fetch_format":"auto",
            "angle":"exif", 
            "effect":"auto_contrast",
            "width": 1000, 
            }, 
        verbose_name='画像',
        )
    brand = models.CharField('ブランド', max_length=200, null=True, blank=True)
    category = models.CharField('分類', max_length=200, null=True, blank=True)
    description = models.TextField('詳細', null=True, blank=True)
    rating = models.DecimalField('レート', max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField('レビュー数', null=True, blank=True, default=0)
    price = models.PositiveIntegerField('価格', null=True, blank=True)
    countInStock = models.PositiveIntegerField('在庫', null=True, blank=True, default=0)
    createdAt = models.DateTimeField('登録日時', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='商品')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='ユーザー')
    name = models.CharField('名称', max_length=200, null=True, blank=True)
    rating = models.IntegerField('レート', null=True, blank=True, default=0)
    comment = models.TextField('コメント', null=True, blank=True)
    createdAt = models.DateTimeField('登録日時', auto_now_add=True)

    def __str__(self):
        return str(self.rating)

    class Meta:
        verbose_name = 'レビュー'
        verbose_name_plural = 'レビュー'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='ユーザー')
    paymentMethod = models.CharField('支払方法', max_length=200, null=True, blank=True)
    taxPrice = models.PositiveIntegerField('税額', null=True, blank=True)
    shippingPrice = models.PositiveIntegerField('送料', null=True, blank=True)
    totalPrice = models.PositiveIntegerField('合計金額', null=True, blank=True)
    isPaid = models.BooleanField('支払済', default=False)
    paidAt = models.DateTimeField('支払日時', auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField('発送済', default=False)
    deliveredAt = models.DateTimeField('発送日時', auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField('登録日', auto_now_add=True)

    def __str__(self):
        return str(self.createdAt)

    class Meta:
        verbose_name = '注文情報'
        verbose_name_plural = '注文情報'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='商品')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='注文')
    name = models.CharField('名前', max_length=200, null=True, blank=True)
    qty = models.PositiveIntegerField('数量', null=True, blank=True, default=0)
    price = models.PositiveIntegerField('価格', null=True, blank=True)
    image = models.CharField('画像', max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = '注文アイテム'
        verbose_name_plural = '注文アイテム'


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True, verbose_name='注文')
    address = models.CharField('住所', max_length=200, null=True, blank=True)
    city = models.CharField('市町村', max_length=200, null=True, blank=True)
    postalCode = models.CharField('郵便番号', max_length=200, null=True, blank=True)
    country = models.CharField('都道府県', max_length=200, null=True, blank=True)
    shippingPrice = models.PositiveIntegerField('', null=True, blank=True)

    def __str__(self):
        return str(self.address)

    class Meta:
        verbose_name = '配送先'
        verbose_name_plural = '配送先'


class Contact(models.Model):
    name = models.CharField('名前', max_length=300, null=True, blank=True)
    email = models.EmailField('Eメール', null=True, blank=True)
    subject = models.CharField('件名', max_length=500, null=True, blank=True)
    message = models.TextField('メッセージ', null=True, blank=True)
    is_finished = models.BooleanField('完了済', null=True, default=False)
    note = models.CharField('メモ', max_length=700, null=True, blank=True)
    created = models.DateField('登録日時', null=True, auto_now_add=True)
