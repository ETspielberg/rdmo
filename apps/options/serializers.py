from rest_framework import serializers

from apps.conditions.models import Condition

from .models import OptionSet, Option
from .validators import OptionSetUniqueKeyValidator, OptionUniquePathValidator


class OptionSetIndexOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'path',
            'text'
        )


class OptionSetIndexSerializer(serializers.ModelSerializer):

    options = OptionSetIndexOptionsSerializer(many=True)

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'key',
            'options'
        )


class OptionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'conditions'
        )
        validators = (OptionSetUniqueKeyValidator(),)


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'optionset',
            'uri_prefix',
            'key',
            'comment',
            'order',
            'text_en',
            'text_de',
            'additional_input'
        )
        validators = (OptionUniquePathValidator(),)


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'key'
        )


class ExportOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'uri',
            'comment',
            'order',
            'text_en',
            'text_de',
            'additional_input'
        )


class ExportConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'uri',
        )


class ExportSerializer(serializers.ModelSerializer):

    options = ExportOptionSerializer(many=True)
    conditions = ExportConditionSerializer(many=True)

    class Meta:
        model = OptionSet
        fields = (
            'uri',
            'comment',
            'order',
            'options',
            'conditions'
        )
