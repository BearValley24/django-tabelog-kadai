# Generated by Django 4.2.11 on 2024-06-20 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='reviewStar',
            field=models.CharField(blank=True, choices=[('1', '★'), ('2', '★★'), ('3', '★★★'), ('4', '★★★★'), ('5', '★★★★★')], max_length=20, verbose_name='reviewStar'),
        ),
    ]
