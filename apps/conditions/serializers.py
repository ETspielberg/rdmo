from rest_framework import serializers

from apps.domain.models import Attribute
from apps.options.models import OptionSet, Option

from .models import *


class ConditionIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'identifier',
            'comment',
            'source_label',
            'relation_label',
            'target_label'
        )


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'identifier',
            'uri',
            'comment',
            'source',
            'relation',
            'target_text',
            'target_option'
        )


class AttributeOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'order',
            'text'
        )


class AttributeSerializer(serializers.ModelSerializer):

    options = AttributeOptionSerializer(many=True)

    class Meta:
        model = Attribute
        fields = (
            'id',
            'label',
            'options'
        )


class OptionSetOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'order',
            'text'
        )


class OptionSetSerializer(serializers.ModelSerializer):

    conditions = OptionSetOptionSerializer(many=True)

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'order',
            'options'
        )


class ExportSerializer(serializers.ModelSerializer):

    target_option = serializers.CharField(source='target_option.identifier')

    class Meta:
        model = Condition
        fields = (
            'identifier',
            'uri',
            'comment',
            'source',
            'relation',
            'target_text',
            'target_option'
        )
