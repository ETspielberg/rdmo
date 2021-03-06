from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import (
    TestListViewMixin,
    TestModelAPIViewMixin,
    TestListAPIViewMixin,
    TestRetrieveAPIViewMixin,
    TestUpdateAPIViewMixin,
    TestDeleteAPIViewMixin
)

from apps.conditions.models import Condition
from apps.options.models import OptionSet

from .models import AttributeEntity, Attribute, Range, VerboseName


class DomainTestCase(TestCase):

    fixtures = (
        'auth.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
    )


class DomainTests(TestListViewMixin, DomainTestCase):

    list_url_name = 'domain'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')


class AttributeEntityTests(TestModelAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:entity'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        # get entities and order them by level to delete the entities at the bottom of the tree first
        self.instances = AttributeEntity.objects.filter(attribute=None).order_by('-level')

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class AttributeTests(TestModelAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:attribute'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Attribute.objects.all()

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class RangeTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TestUpdateAPIViewMixin, TestDeleteAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:range'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Range.objects.all()


class VerboseNameTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, TestUpdateAPIViewMixin, TestDeleteAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:verbosename'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = VerboseName.objects.all()


class ValueTypeTests(TestListAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:valuestype'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')


class OptionSetTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:optionset'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = OptionSet.objects.all()


class ConditionTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, DomainTestCase):

    api_url_name = 'domain:condition'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Condition.objects.all()
