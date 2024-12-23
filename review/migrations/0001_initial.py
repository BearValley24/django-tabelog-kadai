# Generated by Django 4.2.11 on 2024-06-19 23:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shops', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewCreated', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('reviewUpdated', models.DateTimeField(blank=True, verbose_name='updated_at')),
                ('reviewStar', models.IntegerField(blank=True, verbose_name='reviewStar')),
                ('reviewComment', models.TextField(blank=True, max_length=30, null=True, verbose_name='reviewComment')),
                ('reviewShopName', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_reviewShopName', to='shops.shop', verbose_name='reviewShopName')),
                ('reviewUserName', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_reviewUserName', to=settings.AUTH_USER_MODEL, verbose_name='reviewUserName')),
            ],
        ),
    ]
