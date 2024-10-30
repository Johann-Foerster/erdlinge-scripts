from tika import parser
from dataclasses import dataclass, field
import glob, csv

pdfs = glob.glob("abrechnungen/2024/*.pdf")
data = []

def get_pages(filename):
    raw_xml = parser.from_file(pdf, xmlContent=True)
    body = raw_xml['content'].split('<body>')[1].split('</body>')[0]
    body_without_tag = body.replace("<p>", "").replace("</p>", "").replace("<div>", "").replace("</div>","").replace("<p />","")
    text_pages = body_without_tag.split("""<div class="page">""")[1:]
    num_pages = len(text_pages)
    if not num_pages==int(raw_xml['metadata']['xmpTPg:NPages']) : #check if it worked correctly
        print("ERROR in page number crosscheck")
        exit(1)
    return text_pages

@dataclass
class Page:
    month_year: str = field()
    name: str = field()
    is_rueckrechnung: bool = field()
    gesamtbrutto: str = field()

    def __init__(self, page: str):
        # Initialize fields with default values
        lines = page.split('\n')


        self.month_year = [line for line in lines if "Gehaltsabrechnung" in line][0].split(" ")[-1]

        self.name = [line for line in lines if " Abteilung" in line][0].split(" Abteilung")[0]

        self.is_rueckrechnung = "Rückrechnung" in page

        bruttolinesplit = [line for line in lines if "GESAMTBRUTTO:" in line][0].split(" ")
        self.gesamtbrutto = bruttolinesplit[1] if len(bruttolinesplit) > 1 else "0,00"

pages = []
for pdf in pdfs:
    text_pages = get_pages(pdf)
    for page in text_pages:
        print(Page(page))
        pages.append(Page(page))


