# Generated by Django 4.2.11 on 2024-05-15 04:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0001_initial'),
        ('accounts', '0010_user_review_shop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='review_shop',
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated_at'),
        ),
        migrations.CreateModel(
            name='ShopReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='comment')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='updated_at')),
                ('shop_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_shop_id', to='shops.shop', verbose_name='shop_id')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_user_id', to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
        ),
    ]
