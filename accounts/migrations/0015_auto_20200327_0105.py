# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-27 05:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_user_carrier'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='img',
            field=models.CharField(blank=True, help_text=b"URL pointing to location of officer's photo", max_length=500, null=True, verbose_name=b'Image'),
        ),
        migrations.AddField(
            model_name='user',
            name='title',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name=b'Officer Position'),
        ),
    ]
