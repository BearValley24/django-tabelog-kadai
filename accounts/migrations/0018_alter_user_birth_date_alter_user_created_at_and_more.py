# Generated by Django 4.2.11 on 2024-10-29 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0007_alter_shop_regularholiday'),
        ('accounts', '0017_alter_user_account_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='誕生日'),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='作成日'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='メールアドレス'),
        ),
        migrations.AlterField(
            model_name='user',
            name='favorite_shop',
            field=models.ManyToManyField(blank=True, related_name='related_favorite_shop', to='shops.shop', verbose_name='お気に入り店舗'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='姓'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='管理者かどうか'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='名'),
        ),
        migrations.AlterField(
            model_name='user',
            name='rank_is_free',
            field=models.BooleanField(default=True, help_text='無料会員ならTrue、デフォルトは無料会員', verbose_name='会員ランク'),
        ),
        migrations.AlterField(
            model_name='user',
            name='shop_review_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_shop_review_comment', to='shops.shop', verbose_name='レビューコメント'),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='更新日'),
        ),
    ]
