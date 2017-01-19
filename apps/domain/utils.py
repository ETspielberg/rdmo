from .models import *


def import_xml(domain_node):

    nsmap = domain_node.nsmap

    for entity_node in domain_node.iterchildren():

        if entity_node.tag == 'entity':
            _import_attribute_entity(entity_node, nsmap)
        else:
            _import_attribute(entity_node, nsmap)


def _import_attribute(attribute_node, nsmap, parent=None):

    try:
        attribute = Attribute.objects.get(
            parent=parent,
            identifier=attribute_node['{%(dc)s}identifier' % nsmap]
        )
    except Attribute.DoesNotExist:
        attribute = Attribute(
            parent=parent,
            identifier=attribute_node['{%(dc)s}identifier' % nsmap]
        )

    attribute.uri = attribute_node['{%(dc)s}uri' % nsmap]
    attribute.comment = attribute_node['{%(dc)s}comment' % nsmap]
    attribute.is_collection = attribute_node.is_collection
    attribute.value_type = attribute_node.value_type
    attribute.unit = attribute_node.unit
    attribute.save()

    if hasattr(attribute_node, 'range'):
        try:
            range = Range.objects.get(attribute=attribute)
        except Range.DoesNotExist:
            range = Range(attribute=attribute)

        range.minimum = attribute_node.range.minimum
        range.maximum = attribute_node.range.maximum
        range.step = attribute_node.range.step
        range.save()

    if hasattr(attribute_node, 'verbosename'):
        try:
            verbosename = VerboseName.objects.get(attribute_entity=attribute)
        except VerboseName.DoesNotExist:
            verbosename = VerboseName(attribute_entity=attribute)

        verbosename.name_en = attribute_node.verbosename.name_en
        verbosename.name_de = attribute_node.verbosename.name_de
        verbosename.name_plural_en = attribute_node.verbosename.name_plural_en
        verbosename.name_plural_de = attribute_node.verbosename.name_plural_de
        verbosename.save()

    if hasattr(attribute_node, 'optionsets'):
        for optionset_node in attribute_node.optionsets.iterchildren():
            try:
                optionset = OptionSet.objects.get(identifier=optionset_node.get('identifier'))
                attribute.optionsets.add(optionset)
            except OptionSet.DoesNotExist:
                pass

    if hasattr(attribute_node, 'conditions'):
        for condition_node in attribute_node.conditions.iterchildren():
            try:
                condition = Condition.objects.get(identifier=condition_node.get('identifier'))
                attribute.conditions.add(condition)
            except Condition.DoesNotExist:
                pass


def _import_attribute_entity(entity_node, nsmap, parent=None):

    try:
        entity = AttributeEntity.objects.get(
            parent=parent,
            identifier=entity_node['{%(dc)s}identifier' % nsmap]
        )
    except AttributeEntity.DoesNotExist:
        entity = AttributeEntity(
            parent=parent,
            identifier=entity_node['{%(dc)s}identifier' % nsmap]
        )

    entity.uri = entity_node['{%(dc)s}uri' % nsmap]
    entity.comment = entity_node['{%(dc)s}comment' % nsmap]
    entity.is_collection = entity_node.is_collection
    entity.save()

    if hasattr(entity_node, 'verbosename'):
        try:
            verbosename = VerboseName.objects.get(attribute_entity=entity)
        except VerboseName.DoesNotExist:
            verbosename = VerboseName(attribute_entity=entity)

        verbosename.name_en = entity_node.verbosename.name_en
        verbosename.name_de = entity_node.verbosename.name_de
        verbosename.name_plural_en = entity_node.verbosename.name_plural_en
        verbosename.name_plural_de = entity_node.verbosename.name_plural_de
        verbosename.save()

    if hasattr(entity_node, 'conditions'):
        for condition_node in entity_node.conditions.iterchildren():
            try:
                condition = Condition.objects.get(identifier=condition_node.get('identifier'))
                attribute.conditions.add(condition)
            except Condition.DoesNotExist:
                pass

    if hasattr(entity_node, 'children'):
        for child_node in entity_node.children.iterchildren():
            if child_node.tag == 'attribute':
                _import_attribute(child_node, nsmap, parent=entity)
            else:
                _import_attribute_entity(child_node, nsmap, parent=entity)
