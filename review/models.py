from django.db import models
from accounts.models import User
from shops.models import Shop
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

#User = get_user_model()
#Shop = get_user_model()
# Create your models here.

class Review(models.Model):
    Star = (
        ('1', '★'),
        ('2', '★★'),
        ('3', '★★★'),
        ('4', '★★★★'),
        ('5', '★★★★★'),
    )
    reviewShopName = models.ForeignKey(
        Shop,
        verbose_name = _('レビュー対象の店舗名'),
        related_name = 'related_reviewShopName',
        blank = True,
        null = True,
        on_delete = models.CASCADE
    )
    reviewUserName = models.ForeignKey(
        User,
        verbose_name = _('レビューしたユーザー名'),
        related_name = 'related_reviewUserName',
        blank = True,
        null = True,
        on_delete = models.CASCADE
    )
    reviewCreated = models.DateTimeField(
        verbose_name =_('作成日時'),
        auto_now_add =True
    )
    reviewUpdated = models.DateTimeField(
        verbose_name =_('更新日時'),
        auto_now = True
    )
    reviewStar = models.CharField(
        verbose_name = _('評価'),
        blank = True,
        max_length = 20,
        choices = Star
    )
    reviewComment = models.TextField(
        verbose_name =_('コメント'),
        blank = True,
        null = True,
        max_length = 100
    )

    USERNAME_FIELD = 'account_id'
