# Generated by Django 4.2.11 on 2024-11-01 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_alter_schedule_end'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='start',
        ),
        migrations.AddField(
            model_name='schedule',
            name='startDate',
            field=models.DateField(default='2024-10-01', null=True, verbose_name='開始日程'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='startHor',
            field=models.TimeField(default='12:00:00', null=True, verbose_name='開始時間'),
        ),
    ]
