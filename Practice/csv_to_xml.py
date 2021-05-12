import csv
import xml_utils

field_mappings = {
    'Course Record - edX Identifier': 'guid',  # currently wrong mapping
    'Course Record - Course Title': 'title',
    'Course Record - About Page URL': 'link',
    'Course Record - Announced On': 'pubDate',
    'Course Record - Brief Description': 'subtitle',
    'Course Record - Course Number': 'code',
    'Course Record - Course Start Date': 'start',
    'Course Record - Course End Date': 'end',
    'Course Record - Course Duration (weeks)': 'length',
    'Course Record - Self-Paced': 'self_paced',
    'Course Record - Subject Field(s)': 'subject',
    'Relationship Type': 'relationship_type',

}


def cleanData(file_name):
    print 'Begin conversion from csv to xml'
    f = open(file_name, 'r')
    csvFile = csv.reader(f)

    data = [row for row in csvFile]
    f.close()
    headerFromCsv = data[0]
    headersToInclude = [i for i in headerFromCsv if i in field_mappings]
    indices = [headerFromCsv.index(i) for i in headersToInclude]
    dataMunched = []
    for row in data:
        dataMunched.append([row[i] for i in indices])
    dataMap = []
    for row in dataMunched[1:]:
        temp = {}
        for i in range(len(row)):
            temp.update({headersToInclude[i]: row[i]})
        dataMap.append(temp)
    result = []
    for row in dataMap:
        temp = {}
        for col in row:
            temp.update({field_mappings[col]: row[col]})
            print col
        result.append(temp)
    return result


# def write_to_file(data,file_name):
# 	print 'Begin write to csv file'
# 	f = open(file_name,'wb')
# 	try:
# 		f.write(str(data))
# 		print 'write success'
# 	except Exception,e:
# 		print 'Write failed'
# 		print str(e)
# 	finally:
# 		f.close()
# 	print 'Finished write_to_csv'


if __name__ == '__main__':
    file_name = 'MOOC_OCW.csv'
    result = cleanData(file_name)
    parent_xml = xml_utils.create_xml_tags()
    for r in result:
        parent_xml.append(xml_utils.convert_json_to_xml(r))
    xml_utils.write_to_file('output.xml', parent_xml)
