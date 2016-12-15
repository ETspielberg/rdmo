import factory

from factory.django import DjangoModelFactory

from ..models import *


class OptionSetFactory(DjangoModelFactory):

    class Meta:
        model = OptionSet

    identifier = 'test'
    order = 1

    @factory.post_generation
    def post_generation(self, create, extracted, **kwargs):
        OptionFactory(optionset=self, identifier='a', order=1, text_en='A', text_de='A')
        OptionFactory(optionset=self, identifier='b', order=2, text_en='B', text_de='B')
        OptionFactory(optionset=self, identifier='c', order=3, text_en='C', text_de='C')
        OptionFactory(optionset=self, identifier='other', order=4, text_en='Other', text_de='Sonstige', additional_input=True)


class OptionFactory(DjangoModelFactory):

    class Meta:
        model = Option

    identifier = 'test'
    order = 1

    text_en = 'text_en'
    text_de = 'text_de'

    additional_input = False
