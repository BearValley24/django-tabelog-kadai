# Generated by Django 4.2.11 on 2024-10-29 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_kiyaku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_id',
            field=models.CharField(max_length=10, unique=True, verbose_name='アカウント名'),
        ),
    ]
