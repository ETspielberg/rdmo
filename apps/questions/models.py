from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.models import Model, TranslationMixin
from apps.domain.models import AttributeEntity

from .managers import QuestionEntityManager


@python_2_unicode_compatible
class Catalog(Model, TranslationMixin):

    identifier = models.SlugField(
        max_length=128, unique=True,
        verbose_name=_('Identifier'),
        help_text=_('The unambiguous internal identifier of this catalog.')
    )
    uri = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this catalog.')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional information about this catalog.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this catalog in lists.')
    )
    title_en = models.CharField(
        max_length=256,
        verbose_name=_('Title (en)'),
        help_text=_('The English title for this catalog.')
    )
    title_de = models.CharField(
        max_length=256,
        verbose_name=_('Title (de)'),
        help_text=_('The German title for this catalog.')
    )

    class Meta:
        ordering = ('order',)
        verbose_name = _('Catalog')
        verbose_name_plural = _('Catalogs')

    def __str__(self):
        return self.label

    @property
    def title(self):
        return self.trans('title')

    @property
    def label(self):
        return self.trans('title')


def post_save_catalog(sender, **kwargs):
    instance = kwargs['instance']

    for section in instance.sections.all():
        section.save()

post_save.connect(post_save_catalog, sender=Catalog)


@python_2_unicode_compatible
class Section(Model, TranslationMixin):

    catalog = models.ForeignKey(
        Catalog, related_name='sections',
        verbose_name=_('Catalog'),
        help_text=_('The catalog this section belongs to.')
    )
    identifier = models.SlugField(
        max_length=128, db_index=True,
        verbose_name=_('Identifier'),
        help_text=_('The unambiguous internal identifier of this section.')
    )
    uri = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this section.')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional information about this section.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this section in lists.')
    )
    title_en = models.CharField(
        max_length=256,
        verbose_name=_('Title (en)'),
        help_text=_('The English title for this section.')
    )
    title_de = models.CharField(
        max_length=256,
        verbose_name=_('Title (de)'),
        help_text=_('The German title for this section.')
    )
    label_en = models.TextField(
        verbose_name=_('Label (en)'),
        help_text=_('The English label for this section (auto-generated).')
    )
    label_de = models.TextField(
        verbose_name=_('Label (de)'),
        help_text=_('The German label for this section (auto-generated).')
    )

    class Meta:
        ordering = ('catalog__order', 'order')
        unique_together = ('catalog', 'identifier')
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        return self.label

    @property
    def title(self):
        return self.trans('title')

    @property
    def label(self):
        return self.trans('label')


def post_save_section(sender, **kwargs):
    instance = kwargs['instance']
    instance.label_en = instance.catalog.title_en + ' / ' + instance.title_en
    instance.label_de = instance.catalog.title_de + ' / ' + instance.title_de

    post_save.disconnect(post_save_section, sender=sender)
    instance.save()
    post_save.connect(post_save_section, sender=sender)

    for subsection in instance.subsections.all():
        subsection.save()

post_save.connect(post_save_section, sender=Section)


@python_2_unicode_compatible
class Subsection(Model, TranslationMixin):

    section = models.ForeignKey(
        Section, related_name='subsections',
        verbose_name=_('Catalog'),
        help_text=_('The section this subsection belongs to.')
    )
    identifier = models.SlugField(
        max_length=128, db_index=True,
        verbose_name=_('Identifier'),
        help_text=_('The unambiguous internal identifier of this subsection.')
    )
    uri = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this subsection.')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional information about this subsection.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this subsection in lists.')
    )
    title_en = models.CharField(
        max_length=256,
        verbose_name=_('Title (en)'),
        help_text=_('The English title for this subsection.')
    )
    title_de = models.CharField(
        max_length=256,
        verbose_name=_('Title (de)'),
        help_text=_('The German title for this subsection.')
    )
    label_en = models.TextField(
        verbose_name=_('Label (en)'),
        help_text=_('The English label for this subsection (auto-generated).')
    )
    label_de = models.TextField(
        verbose_name=_('Label (de)'),
        help_text=_('The German label for this subsection (auto-generated).')
    )

    class Meta:
        ordering = ('section__catalog__order', 'section__order', 'order')
        unique_together = ('section', 'identifier')
        verbose_name = _('Subsection')
        verbose_name_plural = _('Subsections')

    def __str__(self):
        return self.label

    @property
    def title(self):
        return self.trans('title')

    @property
    def label(self):
        return self.trans('label')


def post_save_subsection(sender, **kwargs):
    instance = kwargs['instance']
    instance.label_en = instance.section.label_en + ' / ' + instance.title_en
    instance.label_de = instance.section.label_de + ' / ' + instance.title_de

    post_save.disconnect(post_save_subsection, sender=sender)
    instance.save()
    post_save.connect(post_save_subsection, sender=sender)

    for entity in instance.entities.all():
        entity.save()


post_save.connect(post_save_subsection, sender=Subsection)


class QuestionEntity(Model, TranslationMixin):

    objects = QuestionEntityManager()

    attribute_entity = models.ForeignKey(
        AttributeEntity, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('Attribute entity'),
        help_text=_('The attribute/entity this question belongs to.')
    )
    subsection = models.ForeignKey(
        Subsection, related_name='entities',
        verbose_name=_('Catalog'),
        help_text=_('The section this question belongs to.')
    )
    identifier = models.SlugField(
        max_length=128, db_index=True,
        verbose_name=_('Identifier'),
        help_text=_('The unambiguous internal identifier of this question/questionset.')
    )
    uri = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this question/questionset.')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional information about this question/questionset.')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'),
        help_text=_('The position of this subsection in lists.')
    )
    label_en = models.TextField(
        verbose_name=_('Label (en)'),
        help_text=_('The English label for this question/questionset (auto-generated).')
    )
    label_de = models.TextField(
        verbose_name=_('Label (de)'),
        help_text=_('The German label for this question/questionset (auto-generated).')
    )
    help_en = models.TextField(
        null=True, blank=True,
        verbose_name=_('Help (en)'),
        help_text=_('The English help text for this question/questionset.')
    )
    help_de = models.TextField(
        null=True, blank=True,
        verbose_name=_('Help (de)'),
        help_text=_('The German help text for this question/questionset.')
    )

    class Meta:
        ordering = ('subsection__section__catalog__order', 'subsection__section__order', 'subsection__order', 'order')
        verbose_name = _('QuestionEntity')
        verbose_name_plural = _('QuestionEntities')

    def __str__(self):
        return self.label

    @property
    def help(self):
        return self.trans('help')

    @property
    def label(self):
        return self.trans('label')

    @property
    def is_collection(self):
        if self.attribute_entity:
            return self.attribute_entity.is_collection
        else:
            return False

    @property
    def is_set(self):
        return not hasattr(self, 'question')


def post_save_question_entity(sender, **kwargs):
    instance = kwargs['instance']

    if instance.attribute_entity:
        instance.label_en = instance.subsection.label_en + ' / ' + instance.attribute_entity.label
        instance.label_de = instance.subsection.label_de + ' / ' + instance.attribute_entity.label
    else:
        instance.label_en = instance.subsection.label_en + ' / --'
        instance.label_de = instance.subsection.label_de + ' / --'

    post_save.disconnect(post_save_question_entity, sender=sender)
    instance.save()
    post_save.connect(post_save_question_entity, sender=sender)


post_save.connect(post_save_question_entity, sender=QuestionEntity)


class Question(QuestionEntity):

    WIDGET_TYPE_CHOICES = (
        ('text', 'Text'),
        ('textarea', 'Textarea'),
        ('yesno', 'Yes/No'),
        ('checkbox', 'Checkboxes'),
        ('radio', 'Radio buttons'),
        ('select', 'Select drop-down'),
        ('range', 'Range slider'),
        ('date', 'Date picker'),
    )

    parent = models.ForeignKey(
        QuestionEntity, blank=True, null=True, related_name='questions',
        verbose_name=_('Parent'),
        help_text=_('The question set this question belongs to.')
    )
    text_en = models.TextField(
        verbose_name=_('Text (en)'),
        help_text=_('The English text for this question.')
    )
    text_de = models.TextField(
        verbose_name=_('Text (de)'),
        help_text=_('The German text for this question.')
    )
    widget_type = models.CharField(
        max_length=12, choices=WIDGET_TYPE_CHOICES,
        verbose_name=_('Widget type'),
        help_text=_('Type of widget for this question.')
    )

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    @property
    def text(self):
        return self.trans('text')
