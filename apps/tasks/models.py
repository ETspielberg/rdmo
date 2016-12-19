from __future__ import unicode_literals

import iso8601

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.models import TranslationMixin
from apps.domain.models import Attribute
from apps.conditions.models import Condition


@python_2_unicode_compatible
class Task(TranslationMixin, models.Model):

    identifier = models.SlugField(
        max_length=128, unique=True,
        verbose_name=_('Identifier'),
        help_text=_('The unambiguous internal identifier of this task.')
    )
    uri = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this task.')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional information about this task.')
    )
    attribute = models.ForeignKey(
        Attribute, blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
        verbose_name=_('Attribute'),
        help_text=_('The attribute this task is refering to.')
    )
    time_period = models.DurationField(
        verbose_name=_('Time period'),
        help_text=_('The the time period after this task becomes active.')
    )
    title_en = models.CharField(
        max_length=256,
        verbose_name=_('Title (en)'),
        help_text=_('The English title for this task.')
    )
    title_de = models.CharField(
        max_length=256,
        verbose_name=_('Title (de)'),
        help_text=_('The German title for this task.')
    )

    text_en = models.CharField(
        max_length=256,
        verbose_name=_('Text (en)'),
        help_text=_('The English text for this task.')
    )
    text_de = models.CharField(
        max_length=256,
        verbose_name=_('Text (de)'),
        help_text=_('The German text for this task.')
    )
    conditions = models.ManyToManyField(
        Condition, blank=True,
        verbose_name=_('Conditions'),
        help_text=_('The list of conditions evaluated for this task.')
    )

    class Meta:
        ordering = ('attribute',)
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.title

    @property
    def title(self):
        return self.trans('title')

    @property
    def text(self):
        return self.trans('text')

    @property
    def has_conditions(self):
        return bool(self.conditions.all())

    def get_deadline(self, project, snapshot=None):
        values = project.values.filter(snapshot=snapshot).filter(attribute=self.attribute)

        for value in values:
            try:
                return iso8601.parse_date(value.text) + self.time_period
            except iso8601.ParseError:
                return None
