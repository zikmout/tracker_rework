import os
from urllib.request import urlopen
import ssl
from bs4 import BeautifulSoup
from bs4.element import Comment
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open
import pintell.core.scrapper as scrapper

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def extract_text_from_html(content):
    bs = BeautifulSoup(content, 'lxml')
    texts = bs.findAll(text=True)
    content = list(filter(tag_visible, texts))
    return content

'''
def extract_html(full_url, link):
    print('HTML -> {}'.format(link))
    html = scrapper.get_url_content(full_url + link)
    if html is None:
        return None
    html = html.encode('utf-8')
    bs = BeautifulSoup(html, 'html.parser')
    texts = bs.findAll(text=True)
    extracts = filter(tag_visible, texts)
    return list(extracts)

def read_pdf(pdf_file):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    PDFPage.get_pages(rsrcmgr, device, pdf_file)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content

def extract_pdf(full_url, link):
    print('FULL URL => {}'.format(full_url + link))
    pdf = urlopen(full_url + link)
    #pdf = get_response_from_url(full_url + link)
    #print('PDF ->>>> {}'.format(type(pdf)))
    output_string = read_pdf(pdf)
    print(output_string)
    pdf.close()
'''
