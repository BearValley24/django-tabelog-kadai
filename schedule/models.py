from django.db import models
from django.urls import reverse
from django.shortcuts import render, redirect
from django.conf import settings
from django.db import models
from django.utils import timezone
from accounts.models import User
from datetime import datetime

# Create your models here.

class Schedule(models.Model):
    """予約スケジュール."""
    startHour = models.TimeField('開始時間',null=True, default='12:00:00')
    startDate = models.DateField('開始日程',null=True, default='2024-10-01')
    end = models.DateField('終了時間だが設定不要',max_length=255,null=True,blank=True,default='2024-01-01')
    name = models.CharField('予約者名', max_length=255)
    shop_name = models.CharField('店舗名',max_length=255,null=True)
    yoyaku_id = models.TextField('予約ID',max_length=255,null=True)
    account = models.ForeignKey(User,verbose_name='ユーザー',on_delete=models.CASCADE,null=True,blank=True,related_name='related_account')
    numbers = models.IntegerField('予約人数',null=False, default=1)
    start = models.TextField('エラー回避用',null=True, blank=True)

    def __str__(self):
        if self.startDate and self.startHour:
            # startDateとstartHourを結合してdatetimeオブジェクトを作成
            start_datetime = timezone.make_aware(datetime.combine(self.startDate, self.startHour)) 
            start_str = start_datetime.strftime('%Y/%m/%d %H:%M:%S')
        else:
            start_str = '未設定'
        
        return f'{self.name} {start_str}'