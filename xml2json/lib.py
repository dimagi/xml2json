from __future__ import absolute_import
from __future__ import unicode_literals
import lxml.etree

xml2json_parser = lxml.etree.XMLParser(remove_comments=True, resolve_entities=False)


def xml2json(xml_string):
    """
    raises xml2json.XMLSyntaxError

    """
    xml = get_xml_from_string(xml_string)
    return convert_xml_to_json(xml)


def get_xml_from_string(xml_string):
    try:
        xml = lxml.etree.fromstring(xml_string, parser=xml2json_parser)
    except lxml.etree.XMLSyntaxError:
        # conveniently lxml.etree.XMLSyntaxError equals xml2json.XMLSyntaxError
        raise
    return xml


def convert_xml_to_json(xml, last_xmlns=None):
    tag, xmlns = get_tag_and_xmlns(xml)
    attributes = {}
    for key, value in xml.attrib.items():
        attributes['@{0}'.format(key)] = str(value)

    children = {}
    for child in xml:
        key, value = convert_xml_to_json(child, last_xmlns=xmlns)
        key = str(key)
        if key in children:
            prev_value = children[key]
            if isinstance(prev_value, list):
                prev_value.append(value)
            else:
                children[key] = [prev_value, value]
        else:
            children[key] = value

    text = xml.text or ''
    text = str(text)

    # check for None because you don't want something like
    # {'@xmlns': None, '#text': 'foo'}
    if xmlns not in (last_xmlns, None):
        attributes['@xmlns'] = xmlns

    if attributes or children:
        result = attributes
        result.update(children)
        if text.strip():
            result['#text'] = text
    else:
        result = text

    return tag, result


def get_tag_and_xmlns(xml):
    try:
        tag = str(xml.tag.split('}')[1])
    except IndexError:
        # This case comes up when you have something like
        #     <n0:foo xmlns:n0="http://foo.com/bar">
        #         <bar>baz</bar>
        #     </n0:foo>
        # in which case tag for bar is not '{}bar' but simply 'bar'
        tag = str(xml.tag)
        xmlns = None
    else:
        xmlns = str(xml.tag.split('}')[0][1:])
    return tag, xmlns

