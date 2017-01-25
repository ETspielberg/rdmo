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
        xml.startElement('catalogs', {})

        for catalog in data:
            self._catalog(xml, catalog)

        xml.endElement('catalogs')
        xml.endDocument()
        return stream.getvalue()

    def _catalog(self, xml, catalog):
        xml.startElement('catalog', {})
        self._text_element(xml, 'identifier', {}, catalog["identifier"])
        self._text_element(xml, 'uri', {}, catalog["uri"])
        self._text_element(xml, 'comment', {}, catalog["comment"])
        self._text_element(xml, 'order', {}, catalog["order"])
        self._text_element(xml, 'title', {'lang': 'en'}, catalog["title_en"])
        self._text_element(xml, 'title', {'lang': 'de'}, catalog["title_de"])

        if 'sections' in catalog and catalog['sections']:
            xml.startElement('sections', {})

            for section in catalog['sections']:
                self._section(xml, section)

            xml.endElement('sections')

        xml.endElement('catalog')

    def _section(self, xml, section):
        xml.startElement('section', {})
        self._text_element(xml, 'identifier', {}, section["identifier"])
        self._text_element(xml, 'uri', {}, section["uri"])
        self._text_element(xml, 'comment', {}, section["comment"])
        self._text_element(xml, 'order', {}, section["order"])
        self._text_element(xml, 'title', {'lang': 'en'}, section["title_en"])
        self._text_element(xml, 'title', {'lang': 'de'}, section["title_de"])

        if 'subsections' in section and section['subsections']:
            xml.startElement('subsections', {})

            for subsection in section['subsections']:
                self._subsection(xml, subsection)

            xml.endElement('subsections')

        xml.endElement('section')

    def _subsection(self, xml, subsection):
        xml.startElement('subsection', {})
        self._text_element(xml, 'identifier', {}, subsection["identifier"])
        self._text_element(xml, 'uri', {}, subsection["uri"])
        self._text_element(xml, 'comment', {}, subsection["comment"])
        self._text_element(xml, 'order', {}, subsection["order"])
        self._text_element(xml, 'title', {'lang': 'en'}, subsection["title_en"])
        self._text_element(xml, 'title', {'lang': 'de'}, subsection["title_de"])

        if 'entities' in subsection and subsection['entities']:
            xml.startElement('entities', {})

            for questionentity in subsection['entities']:
                if 'is_set' in questionentity and questionentity['is_set']:
                    self._questionset(xml, questionentity)
                else:
                    self._question(xml, questionentity)

            xml.endElement('entities')

        xml.endElement('subsection')

    def _question(self, xml, question):
        xml.startElement('question', {})
        self._text_element(xml, 'identifier', {}, question["identifier"])
        self._text_element(xml, 'uri', {}, question["uri"])
        self._text_element(xml, 'comment', {}, question["comment"])
        self._text_element(xml, 'order', {}, question["order"])
        self._text_element(xml, 'text', {'lang': 'en'}, question["text_en"])
        self._text_element(xml, 'text', {'lang': 'de'}, question["text_de"])
        self._text_element(xml, 'help', {'lang': 'en'}, question["help_en"])
        self._text_element(xml, 'help', {'lang': 'de'}, question["help_de"])
        self._text_element(xml, 'widget_type', {}, question["widget_type"])
        self._text_element(xml, 'attribute_entity', question["attribute_entity"], None)
        xml.endElement('question')

    def _questionset(self, xml, questionset):
        xml.startElement('questionset', {})
        self._text_element(xml, 'identifier', {}, questionset["identifier"])
        self._text_element(xml, 'uri', {}, questionset["uri"])
        self._text_element(xml, 'comment', {}, questionset["comment"])
        self._text_element(xml, 'order', {}, questionset["order"])
        self._text_element(xml, 'help', {'lang': 'en'}, questionset["help_en"])
        self._text_element(xml, 'help', {'lang': 'de'}, questionset["help_de"])
        self._text_element(xml, 'attribute_entity', questionset["attribute_entity"], None)

        xml.startElement('questions', {})

        for question in questionset['questions']:
            self._question(xml, question)

        xml.endElement('questions')

        xml.endElement('questionset')

    def _text_element(self, xml, tag, attr, text):
        xml.startElement(tag, attr)
        if text is not None:
            xml.characters(smart_text(text))
        xml.endElement(tag)
