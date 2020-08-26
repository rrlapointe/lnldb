# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-28 22:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20200606_0052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('last_name', 'first_name', 'class_year'), 'permissions': (('change_group', 'Change the group membership of a user'), ('edit_mdc', 'Change the MDC of a user'), ('read_user', 'View users'), ('view_member', 'View LNL members'))},
        ),
    ]