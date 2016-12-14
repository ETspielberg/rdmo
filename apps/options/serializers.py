from rest_framework import serializers

from .models import *


class OptionSetIndexOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'identifier',
            'text'
        )


class OptionSetIndexSerializer(serializers.ModelSerializer):

    options = OptionSetIndexOptionsSerializer(many=True)

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'identifier',
            'options'
        )


class OptionSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionSet
        fields = (
            'id',
            'identifier',
            'uri',
            'comment',
            'order',
            'conditions'
        )


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'id',
            'optionset',
            'identifier',
            'uri',
            'comment',
            'order',
            'text_en',
            'text_de',
            'additional_input'
        )


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = (
            'id',
            'title'
        )


class ExportOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'identifier',
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
            'title',
        )


class ExportSerializer(serializers.ModelSerializer):

    options = ExportOptionSerializer(many=True)
    conditions = ExportConditionSerializer(many=True)

    class Meta:
        model = OptionSet
        fields = (
            'identifier',
            'uri',
            'comment',
            'order',
            'options',
            'conditions'
        )
