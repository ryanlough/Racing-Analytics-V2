#!/usr/bin/env python
import datetime
import io
import requests
import sys

from lxml import html
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams

TRACKS = {
        "saratoga": "SAR",
        }
QUERY = "http://web.archive.org/web/*/http://www.equibase.com/premium/*"
BASE_EQUIBASE_URL = "http://www.equibase.com/premium/eqbPDFChartPlus.cfm?RACE=A"
BASE_ARCHIVE_URL = "http://web.archive.org/web/"

"RACE=A&BorP=P&TID={0}&CTRY={1}&DT={2}&DAY=D&STYLE=EQB"


def update_links(file_name="all_links.dat"):
    print("Updating links...")
    r = requests.get(QUERY)
    r.raise_for_status()
    tree = html.fromstring(r.content)
    links = tree.xpath("//td[@class=\"url\"]/a/text()")
    matches = (link for link in links if link.startswith(BASE_EQUIBASE_URL))
    # Links is huge, get it out of memory asap
    del links

    with open(file_name, 'w') as f:
        for url in matches:
            print(url, file=f)
    print("Done updating links.")

def extract_from_pdf(url):
    r = requests.get(url)
    r.raise_for_status()
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    interpreter = PDFPageInterpreter(rsrcmgr, device)

    pdf = r.content.replace(b'\x00', b'')
    with open(pdf, 'rb') as p:
        for page in PDFPage.get_pages(p):
            import pdb; pdb.set_trace()

def scrape_data(file_name="all_links.dat"):
    with open(file_name) as f:
        urls = (BASE_ARCHIVE_URL + line.rstrip('\n') for line in f)
        for url in urls:
            extract_from_pdf(url)
    
if __name__ == "__main__":
    print("^^^^^^^^^^BEGIN GATHERING DATA^^^^^^^^^^")
    #update_links()
    scrape_data()
    print("^^^^^^^^^^DONE  GATHERING DATA^^^^^^^^^^")
