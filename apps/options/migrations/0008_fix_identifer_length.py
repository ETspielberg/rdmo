# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-19 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('options', '0007_typo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='identifier',
            field=models.SlugField(help_text='The unambiguous internal identifier of this option.', max_length=128, verbose_name='Identifier'),
        ),
        migrations.AlterField(
            model_name='optionset',
            name='identifier',
            field=models.SlugField(help_text='The unambiguous internal identifier of this option set.', max_length=128, unique=True, verbose_name='Identifier'),
        ),
    ]
