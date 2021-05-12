from xml.etree import ElementTree as etree
import os


def retrieve_archived_courses():
    filepath = os.path.join('./', 'archived_courses.xml')
    xmlFile = open(filepath, 'rb')
    # parser = etree.XMLParser(recover=True)
    #parser = etree.XMLParser()
    tree = etree.parse(xmlFile).getroot()
    archived_items = tree.findall('.//item')
    xmlFile.close()
    return archived_items


def merge_with_mitx_feeds(archived_items):
    filepath = os.path.join('./', 'mitx_feeds.xml')
    xmlFile = open(filepath, 'rb')
    parser = etree.XMLParser()

    tree = etree.parse(xmlFile, parser=parser).getroot()

    channel = tree.find('channel')

    for item in archived_items:
        channel.append(item)
    items = channel.findall('item')
    for item in items:
        print item.find('course:subject', tree.nsmap).text.encode('utf8')
    print channel[-1].find('course:subtitle', tree.nsmap).text.encode('utf8')

    xmlFile.close()
    et = etree.ElementTree(tree)

    et.write('newXml.xml', encoding="utf-8", pretty_print=True, exclusive=True)

    # filepath = os.path.join('./','newXml.xml')
    # xmlFile = codecs.open(filepath,mode='w',encoding='utf8')
    # xmlFile.write(xmlStr)


if __name__ == '__main__':
    archived_items = retrieve_archived_courses()
    merge_with_mitx_feeds(archived_items)
