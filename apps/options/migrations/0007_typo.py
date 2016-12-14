# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-14 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('options', '0006_refactoring'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optionset',
            name='conditions',
            field=models.ManyToManyField(blank=True, help_text='The list of conditions evaluated for this option set.', to='conditions.Condition', verbose_name='Conditions'),
        ),
    ]