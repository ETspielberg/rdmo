from apps.domain.models import Attribute
from apps.options.models import Option

from .models import *


def import_xml(conditions_node):

    for condition_node in conditions_node.iterchildren():

        try:
            condition = Condition.objects.get(identifier=condition_node.identifier)
        except Condition.DoesNotExist:
            condition = Condition(identifier=condition_node.identifier)

        condition.identifier = condition_node.identifier
        condition.uri = condition_node.uri
        condition.comment = condition_node.comment
        condition.relation = condition_node.relation
        condition.target_text = condition_node.target_text

        try:
            condition.source = Attribute.objects.get(identifier=condition.source)
        except Attribute.DoesNotExist:
            condition.source = None

        try:
            condition.target_option = Option.objects.get(identifier=condition.source)
        except Option.DoesNotExist:
            condition.target_option = None

        condition.save()
