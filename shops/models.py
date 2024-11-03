from django.db import models
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
#from review.models import Review



# Create your models here.

class ShopTag(models.Model):
    tag = models.CharField(max_length=200)  
    def __str__(self):
        return self.tag

class Shop(models.Model): 
    day = (
        ('7', '定休日無し'),
        ('1', '月曜日'),
        ('2', '火曜日'),
        ('3', '水曜日'),
        ('4', '木曜日'),
        ('5', '金曜日'),
        ('6', '土曜日'),
        ('0', '日曜日')
    )
    ShopTag = models.ManyToManyField(ShopTag, blank=True,verbose_name='カテゴリ') #店舗種別タグ
    shopName = models.CharField(max_length=20, verbose_name='店名') #店名
    phoneNumber = models.CharField(max_length=15, blank=True, null=True, verbose_name='電話番号') #電話番号（ハイフン無し）
    address = models.TextField(blank=True, null=True, verbose_name='住所') #住所
    addressLat = models.FloatField(blank=True, null=True, verbose_name='住所緯度') #緯度
    addressLng = models.FloatField(blank=True, null=True, verbose_name='住所経度') #経度
    startHour1 = models.TimeField(blank=True, null=True, verbose_name='昼営業開始時間') #営業開始時間
    endHour1 = models.TimeField(blank=True, null=True, verbose_name='昼営業終了時間') #営業終了時間
    startHour2 = models.TimeField(blank=True, null=True, verbose_name='夜営業開始時間') #営業開始時間
    endHour2 = models.TimeField(blank=True, null=True, verbose_name='夜営業終了時間') #営業終了時間
    image = models.ImageField(blank=True, null=True, verbose_name='店外観写真') #写真
    introduction = models.TextField(blank=True, null=True, verbose_name='店舗紹介文') #紹介文
    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='作成日時') #作成日
    modified = models.DateTimeField(auto_now=True, null=True, verbose_name='更新日時') #更新日
    regularHoliday = models.CharField(max_length=3, choices=day, blank=True, verbose_name='定休日（無入力で定休日無し）') # 定休日
    review = models.ManyToManyField('review.Review', blank=True, verbose_name='店舗レビュー')

    # 昼と夜で分割営業している店の営業時間を設定出来ない
    def __str__(self):
        return self.shopName
    def get_absolute_url(self):
        #return reverse('shops:shop_create')
        return reverse('shops:shop_detail',args=[str(self.pk)])

class RegularHoliday(models.Model):
    day = models.CharField(max_length=3, choices=[
        ('Mon', '月曜日'),
        ('Tue', '火曜日'),
        ('Wed', '水曜日'),
        ('Thu', '木曜日'),
        ('Fri', '金曜日'),
        ('Sat', '土曜日'),
        ('Sun', '日曜日')
    ])

    def __str__(self):
        return self.get_day_display()