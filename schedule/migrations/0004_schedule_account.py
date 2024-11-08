# Generated by Django 4.2.11 on 2024-05-05 19:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0003_schedule_yoyaku_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_account', to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
    ]
