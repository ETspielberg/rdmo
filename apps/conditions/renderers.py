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
        xml.startElement('conditions', {})

        for condition in data:
            self._condition(xml, condition)

        xml.endElement('conditions')
        xml.endDocument()
        return stream.getvalue()

    def _condition(self, xml, condition):
        xml.startElement('condition', {})
        self._text_element(xml, 'identifier', {}, condition["identifier"])
        self._text_element(xml, 'uri', {}, condition["uri"])
        self._text_element(xml, 'comment', {}, condition["comment"])
        self._text_element(xml, 'source', {}, condition["source"])
        self._text_element(xml, 'relation', {}, condition["relation"])
        self._text_element(xml, 'target_text', {}, condition["target_text"])
        self._text_element(xml, 'target_option', {}, condition["target_option"])
        xml.endElement('condition')

    def _text_element(self, xml, tag, condition, text):
        xml.startElement(tag, condition)
        if text is not None:
            xml.characters(smart_text(text))
        xml.endElement(tag)
