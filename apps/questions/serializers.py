from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.domain.models import AttributeEntity, Attribute

from .models import *


class CatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = (
            'id',
            'identifier',
            'uri',
            'comment',
            'order',
            'title',
            'title_en',
            'title_de',
            'title'
        )


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'identifier',
            'uri',
            'comment',
            'catalog',
            'order',
            'title',
            'title_en',
            'title_de'
        )


class SubsectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subsection
        fields = (
            'id',
            'section',
            'identifier',
            'uri',
            'comment',
            'order',
            'title',
            'title_en',
            'title_de',
        )


class QuestionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            'subsection',
            'attribute_entity',
            'identifier',
            'uri',
            'comment',
            'order',
            'help_en',
            'help_de',
        )


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id',
            'subsection',
            'parent',
            'attribute_entity',
            'identifier',
            'uri',
            'comment',
            'order',
            'help_en',
            'help_de',
            'text_en',
            'text_de',
            'widget_type',
        )


class AttributeEntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'label'
        )


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = (
            'id',
            'label'
        )


class CatalogIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = (
            'id',
            'label',
        )


class SectionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'label',
        )


class SubsectionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subsection
        fields = (
            'id',
            'label',
        )


class QuestionSetIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            'label'
        )


class CatalogAttributeEntityNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeEntity
        fields = (
            'id',
            'label',
        )


class CatalogQuestionNestedSerializer(serializers.ModelSerializer):

    attribute_entity = CatalogAttributeEntityNestedSerializer(read_only=True)

    warning = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            'id',
            'identifier',
            'text',
            'attribute_entity',
            'warning'
        )

    def get_warning(self, obj):
        if not obj.attribute_entity:
            return _('No attribute selected.')
        else:
            return None


class CatalogQuestionEntityNestedSerializer(serializers.ModelSerializer):

    questions = CatalogQuestionNestedSerializer(many=True, read_only=True)
    text = serializers.CharField(source='question.text')

    attribute_entity = CatalogAttributeEntityNestedSerializer(read_only=True)

    warning = serializers.SerializerMethodField()

    class Meta:
        model = QuestionEntity
        fields = (
            'id',
            'identifier',
            'subsection',
            'text',
            'is_set',
            'attribute_entity',
            'questions',
            'warning'
        )

    def get_warning(self, obj):
        if obj.is_set:
            if not obj.attribute_entity:
                return _('No entity selected.')
            else:
                descendants = obj.attribute_entity.get_descendants()

                for question in obj.questions.all():
                    if question.attribute_entity and question.attribute_entity not in descendants:
                        return _('Entity and questions attributes mismatch.')
                        break

                return None
        else:
            if not obj.attribute_entity:
                return _('No attribute selected.')
            else:
                return None


class CatalogSubsectionNestedSerializer(serializers.ModelSerializer):

    entities = serializers.SerializerMethodField()

    class Meta:
        model = Subsection
        fields = (
            'id',
            'identifier',
            'title',
            'entities'
        )

    def get_entities(self, obj):
        entities = QuestionEntity.objects.filter(subsection=obj, question__parent=None).order_by('order')
        serializer = CatalogQuestionEntityNestedSerializer(instance=entities, many=True)
        return serializer.data


class CatalogSectionNestedSerializer(serializers.ModelSerializer):

    subsections = CatalogSubsectionNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = (
            'id',
            'identifier',
            'title',
            'subsections'
        )


class CatalogNestedSerializer(serializers.ModelSerializer):

    sections = CatalogSectionNestedSerializer(many=True, read_only=True)

    urls = serializers.SerializerMethodField()

    class Meta:
        model = Catalog
        fields = (
            'id',
            'identifier',
            'title',
            'title_en',
            'title_de',
            'sections',
            'urls'
        )

    def get_urls(self, obj):
        urls = {}
        for format in settings.EXPORT_FORMATS:
            urls[format] = reverse('questions_catalog_export', args=[obj.pk, format])
        return urls


class ExportAttributeEntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeEntity
        fields = (
            'identifier',
            'label'
        )


class ExportQuestionSerializer(serializers.ModelSerializer):

    attribute_entity = ExportAttributeEntitySerializer()

    class Meta:
        model = Question
        fields = (
            'parent',
            'attribute_entity',
            'identifier',
            'uri',
            'comment',
            'order',
            'help_en',
            'help_de',
            'text_en',
            'text_de',
            'widget_type'
        )


class ExportQuestionEntitySerializer(serializers.ModelSerializer):

    questions = ExportQuestionSerializer(many=True, read_only=True)
    text_en = serializers.CharField(source='question.text_en')
    text_de = serializers.CharField(source='question.text_de')
    widget_type = serializers.CharField(source='question.widget_type')

    attribute_entity = ExportAttributeEntitySerializer(read_only=True)

    class Meta:
        model = QuestionEntity
        fields = (
            'identifier',
            'uri',
            'comment',
            'text_en',
            'text_de',
            'is_set',
            'attribute_entity',
            'order',
            'help_en',
            'help_de',
            'widget_type',
            'questions'
        )


class ExportSubsectionSerializer(serializers.ModelSerializer):

    entities = serializers.SerializerMethodField()

    class Meta:
        model = Subsection
        fields = (
            'identifier',
            'uri',
            'comment',
            'order',
            'title_en',
            'title_de',
            'entities'
        )

    def get_entities(self, obj):
        entities = QuestionEntity.objects.filter(subsection=obj, question__parent=None)
        serializer = ExportQuestionEntitySerializer(instance=entities, many=True)
        return serializer.data


class ExportSectionSerializer(serializers.ModelSerializer):

    subsections = ExportSubsectionSerializer(many=True)

    class Meta:
        model = Catalog
        fields = (
            'identifier',
            'uri',
            'comment',
            'order',
            'title',
            'title_en',
            'title_de',
            'subsections'
        )


class ExportSerializer(serializers.ModelSerializer):

    sections = ExportSectionSerializer(many=True)

    class Meta:
        model = Catalog
        fields = (
            'identifier',
            'uri',
            'comment',
            'order',
            'title',
            'title_en',
            'title_de',
            'sections'
        )
