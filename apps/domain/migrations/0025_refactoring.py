# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-14 14:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0024_meta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attributeentity',
            old_name='description',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='attributeentity',
            old_name='title',
            new_name='identifier',
        ),
    ]
