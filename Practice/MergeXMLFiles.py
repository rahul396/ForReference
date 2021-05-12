from lxml import etree
import os

def retrieve_archived_courses():
	"""Retrieve item tags from mitx_archived_courses.xml to be appended to mitx_feeds.xml """
	print 'Retrieving courses from mitx_archived_courses.xml'
	filepath = './working/mitx_archived_courses.xml'
	xmlFile=None
	archived_items=None
	try:
		xmlFile = open(filepath,'rb')
		parser = etree.XMLParser(recover=True)
		tree  = etree.parse(xmlFile,parser=parser).getroot()
		archived_items = tree.findall('.//item')
	except Exception,e:
		print str(e)
	finally:
		if xmlFile:
			xmlFile.close()
	return archived_items

def merge_with_mitx_feeds(archived_items):
	"""Merge item tags from mitx_archived_courses.xml to mitx_feeds.xml"""
	filepath = './working/mitx_feeds.xml'
	print 'Merging mitx_archived_courses.xml with mitx_feeds.xml'
	try:
		xmlFile = open(filepath,'rb')
		parser = etree.XMLParser(recover=True)
		tree  = etree.parse(xmlFile,parser=parser).getroot()
		channel = tree.find('channel')
		print 'appending mitx archived courses to mitx_feeds.xml'
		for item in archived_items:
			channel.append(item)
		xmlFile.close()
		#Set empty text to include closing tags for empty tags
		items = channel.findall('item')
		for item in items:
			for elem in item.iter():
				if elem.text == None:
					elem.text = ''
		et = etree.ElementTree(tree)
		try:
			et.write(filepath, encoding="utf-8",pretty_print=True,exclusive=True,xml_declaration=True)
			print "Merge Successfull"
		except Exception,e:
			print 'ElementTree write failed: '+str(e)
	except Exception,e:
		print str(e)
		print 'Merge Failed'

if __name__ == '__main__':
	archived_items = retrieve_archived_courses()
	merge_with_mitx_feeds(archived_items)