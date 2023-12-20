# Generated by Django 4.2.6 on 2023-12-19 19:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_blog_author_alter_blog_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='excerpt',
            field=models.TextField(default="Dive into the season of joy and mindfulness with Yogi's Delight! Explore our guide on maintaining serenity amidst the festive bustle. From calming yoga routines to mindful gift-giving, discover how you can infuse your holidays with peace and positivity."),
        ),
        migrations.AlterField(
            model_name='blog',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 19, 19, 17, 41, 293283)),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(default='Yuletide Zen: Finding Balance in Festivity', max_length=255),
        ),
        migrations.AlterField(
            model_name='frontstore',
            name='flash_sale_end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 19, 19, 17, 41, 293283)),
        ),
    ]