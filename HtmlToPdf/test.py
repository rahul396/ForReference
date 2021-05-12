import requests
from fpdf import FPDF, HTMLMixin
from bs4 import BeautifulSoup
import re

url = 'https://www.rba.gov.au/monetary-policy/rba-board-minutes/2018/2018-10-02.html'

# print ('getting page')
resp = requests.get(url)

soup = BeautifulSoup(resp.text, 'html.parser')
documentList = soup.findAll('div',attrs={'class':'column-content content-style'})[0]
#html = documentList.text.encode('latin-1','replace')
html = documentList.__str__()
html = html.strip().encode('utf-8').decode('latin-1')
#print (documentList.__str__().encode('latin-1','ignore'))
#html = '<html><head><meta charset="UTF-8"></head><body>'+html+'</body></html>'
#print (documentList.__str__())
#documentList = documentList.encode('utf-8')

class MyFPDF(FPDF, HTMLMixin):
    def write_pdf(self,html):
        self.add_page()
        self.write_html(html)
        self.output('test.pdf','F')


pdf = MyFPDF()
#pdf.set_compression(0)
#p = zlib.compress(p)
#First page
pdf.add_page()
pdf.write_html(html)
pdf.output('test.pdf','F')
#output = pdf.output('html.pdf', 'S')
# f = open('test.pdf','wb')
# f.write(pdf.buffer.encode("utf-8"))
# f.close()