from collections import defaultdict
import lxml.etree


def xml2json(xml_string):
    """
    raises xml2json.XMLSyntaxError

    """
    try:
        xml = lxml.etree.fromstring(xml_string)
    except lxml.etree.XMLSyntaxError:
        # conveniently lxml.etree.XMLSyntaxError equals xml2json.XMLSyntaxError
        raise

    return convert_xml_to_json(xml)


def convert_xml_to_json(xml, last_xmlns=None):

    tag = unicode(xml.tag.split('}')[1])
    xmlns = unicode(xml.tag.split('}')[0][1:])

    attributes = {}
    for key, value in xml.attrib.items():
        attributes[u'@{0}'.format(key)] = unicode(value)

    children = defaultdict(list)
    for child in xml:
        key, value = convert_xml_to_json(child, last_xmlns=xmlns)
        children[unicode(key)].append(value)

    children = dict((key, value[0] if len(value) == 1 else value)
                    for key, value in children.items())

    text = xml.text or ''
    text = unicode(text)

    if xmlns != last_xmlns:
        attributes[u'@xmlns'] = xmlns

    if attributes or children:
        result = attributes
        result.update(children)
        if text.strip():
            result[u'#text'] = text
    else:
        result = text

    return tag, result
