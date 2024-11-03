from django.db import models
from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from shops.models import Shop

# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, email, account_id, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, account_id=account_id, **extra_fields)
        user.set_password(make_password(password))
        user.save(using=self._db)

        return user

    def create_user(self, email, account_id, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email=email,
            account_id=account_id,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, email, account_id, password, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(
            email=email,
            account_id=account_id,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):

    account_id = models.CharField(
        verbose_name=_("アカウント名"),
        unique=True,
        max_length=10,
    )
    email = models.EmailField(
        verbose_name=_("メールアドレス"),
        unique=True,
    )
    first_name = models.CharField(
        verbose_name=_("姓"),
        max_length=150,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name=_("名"),
        max_length=150,
        null=True,
        blank=True,
    )
    rank_is_free = models.BooleanField(
        verbose_name=_("会員ランク"),
        help_text="無料会員ならTrue、デフォルトは無料会員",
        default=True,
    )
    birth_date = models.DateField(
        verbose_name=_("誕生日"),
        blank=True,
        null=True,
    )
    is_superuser = models.BooleanField(
        verbose_name=_("管理者かどうか"),
        default=False,
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("作成日"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("更新日"),
        auto_now=True,
    )
    favorite_shop = models.ManyToManyField(
        Shop,
        verbose_name=_('お気に入り店舗'),
        blank=True,
        related_name='related_favorite_shop',
    )
    shop_review_comment = models.ForeignKey(
        Shop,
        verbose_name=_('レビューコメント'),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='related_shop_review_comment',
    )

    objects = UserManager()

    USERNAME_FIELD = 'account_id' # ログイン時、ユーザー名の代わりにaccount_idを使用
    REQUIRED_FIELDS = ['email']  # スーパーユーザー作成時にemailも設定する

    def __str__(self):
        return self.account_id
    def yoyaku_id(self):
        return Yoyaku_ID.objects.filter(account=self.account_id)

class Yoyaku_ID(models.Model):
    account = models.ForeignKey(User,verbose_name='ユーザー',on_delete=models.CASCADE,null=True,blank=True,related_name='related_user')
    yoyaku_Id = models.TextField(verbose_name='予約ID',max_length=255,null=True)
    def __str__(self) -> str:
        return self.yoyaku_Id

class Kiyaku(models.Model):
    kiyakuName = models.CharField(verbose_name='規約名称', unique=True, max_length=10)
    kiyakuContent = models.TextField(verbose_name='規約内容',blank=True)
    updated_at = models.DateTimeField(verbose_name=_('最終更新時間'), auto_now=True)
    lastUpdater = models.ForeignKey(User,verbose_name='最終更新者',on_delete=models.CASCADE,blank=True,related_name='last_update_user')
    def __str__(self) -> str:
        return self.kiyakuName