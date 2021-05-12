# from pdfminer.layout import LAParams, LTTextBoxHorizontal
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.converter import PDFPageAggregator
# from pdfminer.pdfpage import PDFPage
# from pdfminer.pdfparser import PDFParser
# from pdfminer.pdfdocument import PDFDocument
# from pdfminer.converter import TextConverter, HTMLConverter
# import io

# def convert(case,fname, pages=None):
#     if not pages: pagenums = set();
#     else:         pagenums = set(pages);      
#     manager = PDFResourceManager() 
#     codec = 'utf-8'
#     caching = True

#     if case == 'text' :
#         output = io.StringIO()
#         converter = TextConverter(manager, output, codec=codec, laparams=LAParams())     
#     if case == 'HTML' :
#         output = io.BytesIO()
#         converter = HTMLConverter(manager, output, codec=codec, laparams=LAParams())

#     interpreter = PDFPageInterpreter(manager, converter)   
#     infile = open(fname, 'rb')

#     for page in PDFPage.get_pages(infile, pagenums,caching=caching, check_extractable=True):
#         interpreter.process_page(page)

#     convertedPDF = output.getvalue()  

#     infile.close(); converter.close(); output.close()
#     return convertedPDF


# print (convert("text", "114666.pdf"))



# from PyPDF2 import PdfFileReader
 
 
# def text_extractor(path):
#     with open(path, 'rb') as f:
#         pdf = PdfFileReader(f)
 
#         # get the first page
#         page = pdf.getPage(2)
#         print(page)
#         print('Page type: {}'.format(str(type(page))))
 
#         text = page.extractText()
#         print(text)
 
 
# if __name__ == '__main__':
#     path = '114666.pdf'
#     text_extractor(path)


# from tika import parser

# raw = parser.from_file('114666.pdf')
# print(raw['content'])


# from PyPDF2 import PdfFileWriter, PdfFileReader

# inputpdf = PdfFileReader(open("114666.pdf", "rb"))
# print (inputpdf.getDocumentInfo())
# output = PdfFileWriter()
# output.addJS("this.print({bUI:true,bSilent:false,bShrinkToFit:true});")
# for i in range(inputpdf.numPages):    
#     output.addPage(inputpdf.getPage(i))

# with open("document-page.pdf", "wb") as outputStream:
#         output.write(outputStream)

import subprocess
subprocess.run(["D:\\qpdf-8.2.1\\bin\\qpdf.exe", "--encrypt", "","", "40","--extract=y","--","114666.pdf", "output.pdf"])
#subprocess.run(["D:\\qpdf-8.2.1\\bin\\qpdf.exe", "--decrypt","output.pdf", "output2.pdf"])
#subprocess.run(["D:\\qpdf-8.2.1\\bin\\qpdf.exe", "--extract=y", "output.pdf", "output2.pdf"])