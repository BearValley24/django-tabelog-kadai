from django.db import models
from accounts.models import User

# Create your models here.

class Subscription(models.Model):
    # 商品名
    name = models.CharField(max_length=100)
    # 商品概要
    description = models.CharField(max_length=255, blank=True, null=True)
    # 商品ID（★stripeの商品IDを値に用いる）
    stripe_product_id = models.CharField(max_length=100)
    # 商品写真登録用のファイル
    file = models.FileField(upload_to="product_files/", blank=True, null=True)
    # 商品詳細ページのリンク
    url  = models.URLField()

    # admin画面で商品名表示
    def __str__(self):
        return self.name

class SubscriptionPrice(models.Model):
    # 外部キーで商品マスタを紐付け
    product = models.ForeignKey(Subscription, related_name='Prices', on_delete=models.CASCADE)
    # 価格ID（★stripeの価格IDを値に用いる）
    stripe_price_id = models.CharField(max_length=100)
    # 価格
    price = models.IntegerField(default=0)
    
    # Django画面に表示する価格
    def get_display_price(self):
        return self.price

# トランザクションマスタ
class Transaction(models.Model):
    # 購入日
    date   = models.CharField(max_length=100)
    # 購入者
    customer_name = models.CharField(max_length=100)
    # 購入者のメールアドレス 購入者名はクレジットカードの名義なのでUserとは一致しない可能性あり
    #email  = models.EmailField(max_length=100)
    email = models.ForeignKey(
        User,
        to_field = 'email',
        verbose_name = 'accounts_email',
        on_delete=models.CASCADE,
        related_name='related_accounts_email',
        )
    # 購入商品名
    product_name = models.CharField(max_length=100)
    # 支払い金額
    product_amount = models.IntegerField()

    # admin画面で商品名表示
    def __str__(self):
        return self.date + '_' + self.product_name  + '_' + self.customer_name