from __future__ import unicode_literals

from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.six.moves import StringIO
from django.utils.encoding import smart_text
from rest_framework.renderers import BaseRenderer


class XMLRenderer(BaseRenderer):

    media_type = 'application/xml'
    format = 'xml'

    def render(self, data):

        if data is None:
            return ''

        stream = StringIO()

        xml = SimplerXMLGenerator(stream, "utf-8")
        xml.startDocument()
        xml.startElement('OptionSets', {})

        for optionset in data:
            self._optionset(xml, optionset)

        xml.endElement('OptionSets')
        xml.endDocument()
        return stream.getvalue()

    def _option(self, xml, option):
        xml.startElement('Option', {})
        self._text_element(xml, 'identifier', {}, option["identifier"])
        self._text_element(xml, 'uri', {}, option["uri"])
        self._text_element(xml, 'comment', {}, option["comment"])
        self._text_element(xml, 'order', {}, option["order"])
        self._text_element(xml, 'text_en', {}, option["text_en"])
        self._text_element(xml, 'text_de', {}, option["text_de"])
        self._text_element(xml, 'additional_input', {}, option["additional_input"])
        xml.endElement('Option')

    def _optionset(self, xml, optionset):
        xml.startElement('OptionSet', {})
        self._text_element(xml, 'identifier', {}, optionset["identifier"])
        self._text_element(xml, 'uri', {}, optionset["uri"])
        self._text_element(xml, 'comment', {}, optionset["comment"])
        self._text_element(xml, 'order', {}, optionset["order"])

        if 'options' in optionset and optionset['options']:
            xml.startElement('Options', {})

            for option in optionset['options']:
                self._option(xml, option)

            xml.endElement('Options')

        if 'conditions' in optionset and optionset['conditions']:
            xml.startElement('Conditions', {})

            for condition in optionset['conditions']:
                self._condition(xml, condition)

            xml.endElement('Conditions')

        xml.endElement('OptionSet')

    def _condition(self, xml, condition):
        xml.startElement('Condition', {})
        self._text_element(xml, 'identifier', {}, condition["identifier"])
        xml.endElement('Condition')

    def _text_element(self, xml, tag, option, text):
        xml.startElement(tag, option)
        if text is not None:
            xml.characters(smart_text(text))
        xml.endElement(tag)