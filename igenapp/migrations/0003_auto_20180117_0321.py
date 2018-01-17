# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-17 03:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('igenapp', '0002_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(default='somebody@example.com', max_length=80),
        ),
        migrations.AddField(
            model_name='user',
            name='first_Name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='last_Name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='password', max_length=40),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='somebody', max_length=40),
        ),
    ]
