# Generated by Django 4.2.11 on 2024-06-11 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_shopreview_unique_together'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShopReview',
        ),
    ]
