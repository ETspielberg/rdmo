from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from apps.core.models import TranslationMixin
from apps.conditions.models import Condition


@python_2_unicode_compatible
class AttributeEntity(MPTTModel):

    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children', db_index=True,
        verbose_name=_('Parent entity'),
        help_text=_('Parent entity in the domain model.')
    )
    identifier = models.SlugField(
        max_length=128,
        verbose_name=_('Identifier'),
        help_text=_('Unambiguous internal identifier of this attribute/entity.')
    )
    uri = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('Uniform Resource Identifier of this attribute/entity.')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional information about this attribute/entity.')
    )
    label = models.CharField(
        max_length=512, db_index=True,
        verbose_name=_('Label'),
        help_text=_('Full identifier of this attribute/entity (auto-generated).')
    )
    is_collection = models.BooleanField(
        default=False,
        verbose_name=_('is collection'),
        help_text=_('Designates whether this attribute/entity is a collection.')
    )
    is_attribute = models.BooleanField(
        default=False,
        verbose_name=_('is attribute'),
        help_text=_('Designates whether this attribute/entity is an attribute (auto-generated).')
    )
    parent_collection = models.ForeignKey(
        'AttributeEntity', blank=True, null=True, default=None, related_name='+', db_index=True,
        verbose_name=_('Parent collection'),
        help_text=_('Next collection entity upwards in the domain model (auto-generated).')
    )
    conditions = models.ManyToManyField(
        Condition, blank=True,
        verbose_name=_('Conditions'),
        help_text=_('List of conditions evaluated for this attribute/entity.')
    )

    class Meta:
        ordering = ('label', )
        verbose_name = _('Attribute entity')
        verbose_name_plural = _('Attribute entities')

    class MPTTMeta:
        order_insertion_by = ['identifier']

    def __str__(self):
        return self.label

    @property
    def range(self):
        if self.is_attribute:
            return self.attribute.range
        else:
            return None

    @property
    def has_options(self):
        if self.is_attribute:
            return bool(self.attribute.options.all())
        else:
            return False

    @property
    def has_conditions(self):
        return bool(self.conditions.all())


@python_2_unicode_compatible
class Attribute(AttributeEntity):

    VALUE_TYPE_TEXT = 'text'
    VALUE_TYPE_URL = 'url'
    VALUE_TYPE_INTEGER = 'integer'
    VALUE_TYPE_FLOAT = 'float'
    VALUE_TYPE_BOOLEAN = 'boolean'
    VALUE_TYPE_DATETIME = 'datetime'
    VALUE_TYPE_OPTIONS = 'options'
    VALUE_TYPE_CHOICES = (
        (VALUE_TYPE_TEXT, _('Text')),
        (VALUE_TYPE_URL, _('URL')),
        (VALUE_TYPE_INTEGER, _('Integer')),
        (VALUE_TYPE_FLOAT, _('Float')),
        (VALUE_TYPE_BOOLEAN, _('Boolean')),
        (VALUE_TYPE_DATETIME, _('Datetime')),
        (VALUE_TYPE_OPTIONS, _('Options'))
    )

    value_type = models.CharField(
        max_length=8, choices=VALUE_TYPE_CHOICES,
        verbose_name=_('Value type'),
        help_text=_('Type of values for this attribute.')
    )
    unit = models.CharField(
        max_length=64, blank=True, null=True,
        verbose_name=_('Unit'),
        help_text=_('Unit of values for this attribute.')
    )

    optionsets = models.ManyToManyField(
        'options.OptionSet', blank=True,
        verbose_name=_('Option sets'),
        help_text=_('Option sets for this attribute.')
    )

    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')

    def __str__(self):
        return self.label

    @property
    def options(self):
        options_list = []
        for optionset in self.optionsets.all():
            options_list += optionset.options.all()

        return options_list


def post_save_attribute_entity(sender, **kwargs):

    if not kwargs['raw']:
        instance = kwargs['instance']

        # init fields
        instance.label = instance.identifier
        instance.is_attribute = hasattr(instance, 'attribute')
        instance.parent_collection = None

        # set parent_collection if the entity is a collection itself
        if instance.is_collection and not instance.is_attribute:
            instance.parent_collection = instance

        # loop over parents
        parent = instance.parent
        while parent:
            # set parent_collection if it is not yet set and if parent is a collection
            if not instance.parent_collection and parent.is_collection:
                instance.parent_collection = parent

            # update own full name
            instance.label = parent.identifier + '.' + instance.label

            parent = parent.parent

        post_save.disconnect(post_save_attribute_entity, sender=sender)
        instance.save()
        post_save.connect(post_save_attribute_entity, sender=sender)

        # update the full name and parent_collection of children
        # this makes it recursive
        for child in instance.children.all():
            child.save()


post_save.connect(post_save_attribute_entity, sender=AttributeEntity)
post_save.connect(post_save_attribute_entity, sender=Attribute)


@python_2_unicode_compatible
class VerboseName(models.Model, TranslationMixin):

    attribute_entity = models.OneToOneField(
        'AttributeEntity',
        verbose_name=_('Attribute entity'),
        help_text=_('Attribute/entity this verbose name belongs to.')
    )
    name_en = models.CharField(
        max_length=256,
        verbose_name=_('Name (en)'),
        help_text=_('English name displayed for this attribute/entity (e.g. project).')
    )
    name_de = models.CharField(
        max_length=256,
        verbose_name=_('Name (de)'),
        help_text=_('German name displayed for this attribute/entity (e.g. Projekt).')
    )
    name_plural_en = models.CharField(
        max_length=256,
        verbose_name=_('Plural name (en)'),
        help_text=_('English plural name displayed for this attribute/entity (e.g. projects).')
    )
    name_plural_de = models.CharField(
        max_length=256,
        verbose_name=_('Plural name (de)'),
        help_text=_('German plural name displayed for this attribute/entity (e.g. Projekte).')
    )

    class Meta:
        verbose_name = _('Verbose name')
        verbose_name_plural = _('Verbose names')

    def __str__(self):
        return self.attribute_entity.label

    @property
    def name(self):
        return self.trans('name')

    @property
    def name_plural(self):
        return self.trans('name_plural')


@python_2_unicode_compatible
class Range(models.Model, TranslationMixin):

    attribute = models.OneToOneField(
        'Attribute',
        verbose_name=_('Attribute'),
        help_text=_('Attribute this verbose name belongs to.')
    )
    minimum = models.FloatField(
        verbose_name=_('Minimum'),
        help_text=_('Minimal value for this attribute.')
    )
    maximum = models.FloatField(
        verbose_name=_('Maximum'),
        help_text=_('Maximum value for this attribute.')
    )
    step = models.FloatField(
        verbose_name=_('Step'),
        help_text=_('Step in which this attribute can be incremented/decremented.')
    )

    class Meta:
        ordering = ('attribute', )
        verbose_name = _('Range')
        verbose_name_plural = _('Ranges')

    def __str__(self):
        return self.attribute.label
