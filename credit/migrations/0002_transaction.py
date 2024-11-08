# Generated by Django 4.2.11 on 2024-05-06 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=100)),
                ('customer_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('product_name', models.CharField(max_length=100)),
                ('product_amount', models.IntegerField()),
            ],
        ),
    ]
