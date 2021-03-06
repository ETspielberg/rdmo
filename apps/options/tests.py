from django.test import TestCase
from django.utils import translation

from apps.core.testing.mixins import (
    TestListViewMixin,
    TestModelAPIViewMixin,
    TestListAPIViewMixin,
    TestRetrieveAPIViewMixin
)

from apps.conditions.models import Condition

from .models import OptionSet, Option


class OptionsTestCase(TestCase):

    fixtures = (
        'auth.json',
        'accounts.json',
        'conditions.json',
        'domain.json',
        'options.json',
    )


class OptionsTests(TestListViewMixin, OptionsTestCase):

    list_url_name = 'options'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')


class OptionSetTests(TestModelAPIViewMixin, OptionsTestCase):

    api_url_name = 'options:optionset'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = OptionSet.objects.all()

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class OptionTests(TestModelAPIViewMixin, OptionsTestCase):

    api_url_name = 'options:option'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Option.objects.all()

    def prepare_create_instance(self, instance):
        instance.key += '_new'
        return instance


class ConditionTests(TestListAPIViewMixin, TestRetrieveAPIViewMixin, OptionsTestCase):

    api_url_name = 'options:condition'

    def setUp(self):
        translation.activate('en')
        self.client.login(username='admin', password='admin')
        self.instances = Condition.objects.all()
