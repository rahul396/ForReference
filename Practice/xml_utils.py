from lxml import etree
import os as operatingSystem


def create_xml_tags():
    # define a namespace
    nsmap = {'course': 'https://www.edx.org/api/course/elements/1.0/',
             'staff': 'https://www.edx.org/api/staff/elements/1.0/',
             'dc': 'http://purl.org/dc/elements/1.1/',
             'atom': 'http://www.w3.org/2005/Atom'}
    xml_tags = {}
    # Now create xml tags using lxml.etree module
    xml_tags['rss'] = etree.Element("rss", nsmap=nsmap)
    xml_tags['channel'] = etree.SubElement(xml_tags['rss'], "channel")
    xml_tags['item'] = etree.SubElement(xml_tags['channel'], "item")
    xml_tags['guid'] = etree.SubElement(xml_tags['item'], 'guid')
    xml_tags['title'] = etree.SubElement(xml_tags['item'], 'title')
    xml_tags['link'] = etree.SubElement(xml_tags['item'], 'link')
    xml_tags['pubDate'] = etree.SubElement(xml_tags['item'], 'pubDate')
    xml_tags['course_subtitle'] = etree.SubElement(xml_tags['item'], '{%s}subtitle' % (nsmap['course']))
    xml_tags['course_code'] = etree.SubElement(xml_tags['item'], '{%s}code' % (nsmap['course']))
    xml_tags['course_start'] = etree.SubElement(xml_tags['item'], '{%s}start' % (nsmap['course']))
    xml_tags['course_end'] = etree.SubElement(xml_tags['item'], "{%s}end" % (nsmap['course']))
    xml_tags['course_length'] = etree.SubElement(xml_tags['item'], "{%s}length" % (nsmap['course']))
    xml_tags['course_self_paced'] = etree.SubElement(xml_tags['item'], '{%s}self_paced' % (nsmap['course']))
    # xml_tags['course_profed']= etree.SubElement(xml_tags['item'], '{%s}profed' % (nsmap['course']))
    # xml_tags['course_image_thumbnail']= etree.SubElement(xml_tags['item'], '{%s}image-thumbnail' % (nsmap['course']))
    xml_tags['course_subject'] = etree.SubElement(xml_tags['item'], '{%s}subject' % (nsmap['course']))
    xml_tags['course_school'] = etree.SubElement(xml_tags['item'], '{%s}school' % (nsmap['course']))
    xml_tags['relationship_type'] = etree.SubElement(xml_tags['item'], '{%s}relationship_type' % (nsmap['course']))

    return xml_tags['rss']


def convert_json_to_xml(json_data):
    xml_tags = create_xml_tags()
    nsmap = {'course': 'https://www.edx.org/api/course/elements/1.0/',
             'staff': 'https://www.edx.org/api/staff/elements/1.0/',
             'dc': 'http://purl.org/dc/elements/1.1/',
             'atom': 'http://www.w3.org/2005/Atom'}
    item = xml_tags.find('channel').find('item')
    item.find('guid').text = json_data['guid']
    item.find('title').text = json_data['title']
    item.find('link').text = json_data['link']
    item.find('pubDate').text = json_data['pubDate']
    item.find('{%s}subtitle' % (nsmap['course'])).text = json_data['subtitle']
    item.find('{%s}code' % (nsmap['course'])).text = json_data['code']
    item.find('{%s}start' % (nsmap['course'])).text = json_data['start']
    item.find("{%s}end" % (nsmap['course'])).text = json_data['end']
    item.find("{%s}length" % (nsmap['course'])).text = json_data['length']
    item.find('{%s}self_paced' % (nsmap['course'])).text = json_data['self_paced']
    item.find('{%s}subject' % (nsmap['course'])).text = json_data['subject']
    item.find('{%s}school' % (nsmap['course'])).text = 'MITx'
    item.find('{%s}relationship_type' % (nsmap['course'])).text = json_data['relationship_type']

    return xml_tags.find('item')


def write_to_file(filepath, xml_tags):
    if operatingSystem.path.isfile(filepath):
        xmlFile = open(filepath, 'rb')
        parser = etree.XMLParser(recover=True, remove_blank_text=True)

        tree = etree.parse(xmlFile, parser=parser).getroot()

        channel_new = tree.find('channel')
        for tag in xml_tags:
            channel_new.append(tag['item'])
        xmlFile.close()
        et = etree.ElementTree(tree)
        et.write(filepath, encoding="utf-8", pretty_print=True)
    else:
        et = etree.ElementTree(xml_tags['rss'])
        et.write(filepath, encoding="utf-8", pretty_print=True)
    LOG('XML: File write successfull', INFO, etree.tostring(xml_tags['item'], pretty_print=True, encoding="utf-8"))
