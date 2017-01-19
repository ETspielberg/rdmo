from .models import *


def import_xml(optionsets_node):

    for optionset_node in optionsets_node.iterchildren():

        try:
            optionset = OptionSet.objects.get(identifier=optionset_node.identifier)
        except OptionSet.DoesNotExist:
            optionset = OptionSet(identifier=optionset_node.identifier)

        optionset.uri = optionset_node.uri
        optionset.comment = optionset_node.comment
        optionset.order = optionset_node.order
        optionset.save()

        for option_node in optionset_node.options.iterchildren():
            try:
                option = Option.objects.get(optionset=optionset, identifier=option_node.identifier)
            except Option.DoesNotExist:
                option = Option(optionset=optionset, identifier=option_node.identifier)

            option.uri = option_node.uri
            option.comment = option_node.comment
            option.order = option_node.order
            option.text_en = option_node.text_en
            option.text_de = option_node.text_de
            option.additional_input = option_node.additional_input
            option.save()
