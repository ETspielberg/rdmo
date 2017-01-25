# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-19 16:53
from __future__ import unicode_literals

from django.db import migrations
from django.utils.text import slugify


def create_identifier(apps, schema_editor):

    Catalog = apps.get_model('questions', 'Catalog')
    Section = apps.get_model('questions', 'Section')
    Subsection = apps.get_model('questions', 'Subsection')
    QuestionEntity = apps.get_model('questions', 'QuestionEntity')

    for obj in Catalog.objects.all():
        if not obj.identifier:
            obj.identifier = slugify(obj.title_en)
        obj.save()

    for obj in Section.objects.all():
        if not obj.identifier:
            obj.identifier = slugify(obj.title_en)
        obj.save()

    for obj in Subsection.objects.all():
        if not obj.identifier:
            obj.identifier = slugify(obj.title_en)
        obj.save()

    for obj in QuestionEntity.objects.all():
        if not obj.identifier:
            obj.identifier = slugify(obj.attribute_entity.identifier)
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_refactoring'),
    ]

    operations = [
        migrations.RunPython(create_identifier),
    ]
