# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-19 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conditions', '0011_refactoring'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condition',
            name='identifier',
            field=models.SlugField(help_text='The unambiguous internal identifier of this condition.', max_length=128, unique=True, verbose_name='Identifier'),
        ),
    ]
