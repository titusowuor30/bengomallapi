# Generated by Django 4.2.6 on 2023-12-18 17:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_emailconfig_alter_blog_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 18, 17, 14, 24, 597483)),
        ),
        migrations.AlterField(
            model_name='frontstore',
            name='flash_sale_end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 18, 17, 14, 24, 597483)),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 18, 17, 14, 24, 597483)),
        ),
    ]