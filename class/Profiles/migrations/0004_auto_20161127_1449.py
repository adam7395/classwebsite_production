# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 22:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profiles', '0003_auto_20161127_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='background',
            field=models.CharField(blank=True, default='What is your education level, were you a 109 student, etc.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.TextField(blank=True, default='Where are you from? What is your science background? What do you hope to gain from the class, etc.', null=True),
        ),
    ]
