from django.contrib import admin
from .models import Subscription, SubscriptionPrice, Transaction

# Register your models here.

# 管理画面に商品マスタと価格マスタを表示
admin.site.register(Subscription)
admin.site.register(SubscriptionPrice)
admin.site.register(Transaction)