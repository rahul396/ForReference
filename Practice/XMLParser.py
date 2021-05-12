from bs4 import BeautifulSoup
import os


class XMLParser:
    def __init__(self, sourceFilePath, destinationFilePath):
        self.sourceFilePath = sourceFilePath
        self.destinationFilePath = destinationFilePath

    def retrieve_archived_courses(self):
        xmlFile = open(self.sourceFilePath, 'rb')
        soup = BeautifulSoup(xmlFile, 'xml')
        archived_items = soup.find_all('item')
        xmlFile.close()
        return archived_items

    def merge_with_mitx_feeds(self, archived_items):
        xmlFile = open(self.destinationFilePath, 'rb')
        soup = BeautifulSoup(xmlFile, 'xml')
        channel = soup.find('channel')
        for item in archived_items:
            channel.append(item)
        items = channel.find_all('item')
        for item in items:
            print item.find('course:subject').text
        xmlFile.close()
        filepath = os.path.join('./', 'newXml.xml')
        newFile = open(filepath, 'wb')
        try:
            newFile.write(str(soup))
            print 'Write complete: ' + filepath
        except Exception, e:
            print str(e)
        finally:
            newFile.close()


if __name__ == '__main__':
    sourceFilePath = os.path.join('./', 'archived_courses.xml')
    destinationFilePath = os.path.join('./', 'mitx_feeds.xml')
    xmlParser = XMLParser(sourceFilePath=sourceFilePath, destinationFilePath=destinationFilePath)
    archived_items = xmlParser.retrieve_archived_courses()
    xmlParser.merge_with_mitx_feeds(archived_items)
