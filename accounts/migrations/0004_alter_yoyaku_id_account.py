# Generated by Django 4.2.11 on 2024-05-04 10:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_yoyaku_id_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yoyaku_id',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_account', to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
    ]
