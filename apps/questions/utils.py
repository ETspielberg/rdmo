from apps.domain.models import AttributeEntity, Attribute

from .models import Catalog, Section, Subsection, QuestionEntity, Question


def import_xml(catalogs_node):

    for catalog_node in catalogs_node.iterchildren():
        import_catalog(catalog_node)


def import_catalog(catalog_node):
    try:
        catalog = Catalog.objects.get(identifier=catalog_node.identifier)
    except Catalog.DoesNotExist:
        catalog = Catalog(identifier=catalog_node.identifier)

    catalog.uri = catalog_node.uri
    catalog.comment = catalog_node.comment
    catalog.order = catalog_node.order
    for element in catalog_node.title:
        setattr(catalog, 'title_' + element.get('lang'), element)

    catalog.save()

    if hasattr(catalog_node, 'sections'):
        for section_node in catalog_node.sections.iterchildren():
            import_section(section_node, catalog=catalog)


def import_section(section_node, catalog=None):
    try:
        section = Section.objects.get(catalog=catalog, identifier=section_node.identifier)
    except Section.DoesNotExist:
        section = Section(catalog=catalog, identifier=section_node.identifier)

    section.uri = section_node.uri
    section.comment = section_node.comment
    section.order = section_node.order
    for element in section_node.title:
        setattr(section, 'title_' + element.get('lang'), element)

    section.save()

    if hasattr(section_node, 'subsections'):
        for subsection_node in section_node.subsections.iterchildren():
            import_subsection(subsection_node, section=section)


def import_subsection(subsection_node, section=None):
    try:
        subsection = Subsection.objects.get(section=section, identifier=subsection_node.identifier)
    except Subsection.DoesNotExist:
        subsection = Subsection(section=section, identifier=subsection_node.identifier)

    subsection.uri = subsection_node.uri
    subsection.comment = subsection_node.comment
    subsection.order = subsection_node.order
    for element in subsection_node.title:
        setattr(subsection, 'title_' + element.get('lang'), element)

    subsection.save()
    if hasattr(subsection_node, 'entities'):
        for entity_node in subsection_node.entities.iterchildren():
            if entity_node.tag == 'questionset':
                import_questionset(entity_node, subsection=subsection)
            else:
                import_question(entity_node, subsection=subsection)


def import_questionset(questionset_node, subsection=None):
    try:
        questionset = QuestionEntity.objects.get(subsection=subsection, identifier=questionset_node.identifier, question=None)
    except QuestionEntity.DoesNotExist:
        questionset = QuestionEntity(subsection=subsection, identifier=questionset_node.identifier, question=None)

    questionset.uri = questionset_node.uri
    questionset.comment = questionset_node.comment
    questionset.order = questionset_node.order
    for element in questionset_node['help']:
        setattr(questionset, 'help_' + element.get('lang'), element.text)
    try:
        questionset.attribute_entity = AttributeEntity.objects.get(label=questionset_node.attribute_entity.get('label'))
    except Attribute.DoesNotExist:
        questionset.attribute_entity = None

    questionset.save()

    if hasattr(questionset_node, 'questions'):
        for question_node in questionset_node.questions.iterchildren():
            import_question(question_node, subsection=subsection, parent=questionset)


def import_question(question_node, subsection=None, parent=None):

    try:
        question = Question.objects.get(subsection=subsection, parent=parent, identifier=question_node.identifier)
    except Question.DoesNotExist:
        question = Question(subsection=subsection, parent=parent, identifier=question_node.identifier)

    question.uri = question_node.uri
    question.comment = question_node.comment
    question.order = question_node.order
    question.widget_type = question_node.widget_type
    for element in question_node['text']:
        setattr(question, 'text_' + element.get('lang'), element.text)
    for element in question_node['help']:
        setattr(question, 'help_' + element.get('lang'), element.text)
    try:
        question.attribute_entity = Attribute.objects.get(label=question_node.attribute_entity.get('label'))
    except Attribute.DoesNotExist:
        question.attribute_entity = None

    question.save()
