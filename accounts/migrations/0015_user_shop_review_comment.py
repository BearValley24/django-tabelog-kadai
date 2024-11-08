# Generated by Django 4.2.11 on 2024-06-16 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0001_initial'),
        ('accounts', '0014_delete_shopreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='shop_review_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_shop_review_comment', to='shops.shop', verbose_name='shop_review_comment'),
        ),
    ]
