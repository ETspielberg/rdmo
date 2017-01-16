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
        xml.startElement('domain', {
            'xmlns:dc': "http://purl.org/dc/elements/1.1/"
        })

        for attribute_entity in data:
            if attribute_entity['is_attribute']:
                self._attribute(xml, attribute_entity)
            else:
                self._attribute_entity(xml, attribute_entity)

        xml.endElement('domain')
        xml.endDocument()
        return stream.getvalue()

    def _attribute(self, xml, attribute):
        xml.startElement('attribute', {})
        self._text_element(xml, 'dc:identifier', {}, attribute["identifier"])
        self._text_element(xml, 'dc:uri', {}, attribute["uri"])
        self._text_element(xml, 'dc:comment', {}, attribute["comment"])
        self._text_element(xml, 'is_collection', {}, attribute["is_collection"])
        self._text_element(xml, 'value_type', {}, attribute["value_type"])
        self._text_element(xml, 'unit', {}, attribute["unit"])

        if 'range' in attribute and attribute['range']:
            self._range(xml, attribute['range'])

        if 'verbosename' in attribute and attribute['verbosename']:
            self._verbosename(xml, attribute['verbosename'])

        if 'optionsets' in attribute and attribute['optionsets']:
            xml.startElement('optionsets', {})

            for optionset in attribute['optionsets']:
                xml.startElement('optionset', optionset)
                xml.endElement('optionset')

            xml.endElement('optionsets')

        if 'conditions' in attribute and attribute['conditions']:
            xml.startElement('conditions', {})

            for condition in attribute['conditions']:
                xml.startElement('condition', condition)
                xml.endElement('condition')

            xml.endElement('conditions')

        xml.endElement('attribute')

    def _attribute_entity(self, xml, attribute_entity):
        xml.startElement('entity', {})
        self._text_element(xml, 'dc:identifier', {}, attribute_entity["identifier"])
        self._text_element(xml, 'dc:uri', {}, attribute_entity["uri"])
        self._text_element(xml, 'dc:comment', {}, attribute_entity["comment"])
        self._text_element(xml, 'is_collection', {}, attribute_entity["is_collection"])

        if 'verbosename' in attribute_entity and attribute_entity['verbosename']:
            self._verbosename(xml, attribute_entity['verbosename'])

        if 'conditions' in attribute_entity and attribute_entity['conditions']:
            xml.startElement('conditions', {})

            for condition in attribute_entity['conditions']:
                xml.startElement('condition', condition)
                xml.endElement('condition')

            xml.endElement('conditions')

        if 'children' in attribute_entity:
            xml.startElement('children', {})

            for child in attribute_entity['children']:
                if child['is_attribute']:
                    self._attribute(xml, child)
                else:
                    self._attribute_entity(xml, child)

            xml.endElement('children')

        xml.endElement('entity')

    def _range(self, xml, range):
        xml.startElement('range', {})
        self._text_element(xml, 'minimum', {}, range["minimum"])
        self._text_element(xml, 'maximum', {}, range["maximum"])
        self._text_element(xml, 'step', {}, range["step"])
        xml.endElement('range')

    def _verbosename(self, xml, verbosename):
        xml.startElement('verbosename', {})
        self._text_element(xml, 'name_en', {}, verbosename["name_en"])
        self._text_element(xml, 'name_de', {}, verbosename["name_de"])
        self._text_element(xml, 'name_plural_en', {}, verbosename["name_plural_en"])
        self._text_element(xml, 'name_plural_de', {}, verbosename["name_plural_de"])
        xml.endElement('verbosename')

    def _text_element(self, xml, tag, attributes, text):
        xml.startElement(tag, attributes)
        if text is not None:
            xml.characters(smart_text(text))
        xml.endElement(tag)
