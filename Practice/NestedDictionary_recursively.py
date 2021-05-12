# Example code:

from Products.CMFCore.utils import getToolByName

catalog = getToolByName(context, 'portal_catalog')
path = '/Plone/courses/mechanical-engineering/2-002-circuits-and-electronics-spring-2007'
courses = catalog.searchResults({'meta_type': ('Course'), 'path': {'query': path}})


def get_pdf(obj):
    children = obj.getChildNodes()
    sections = [child for child in children if child.meta_type == 'CourseSection']
    pdfs = [child for child in children if child.virtual_url_path()[-3:] == 'pdf']
    if sections:
        result = {}
        for section in sections:
            result.update({section.id: get_pdf(section)})
        return result
    else:
        return [pdf.virtual_url_path() for pdf in pdfs]


obj = courses[0].getObject()
pdf_list = get_pdf(obj)
print pdf_list

return printed
