# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-03 09:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0012_renaming'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='attribute',
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='attributeentity',
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='attributeentity',
            name='level',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attributeentity',
            name='lft',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attributeentity',
            name='rght',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attributeentity',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attributeentity',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, help_text='optional', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='domain.AttributeEntity'),
        ),
    ]
