from tika import parser
from dataclasses import dataclass, field
import glob, csv, sys

pdfs = glob.glob("abrechnungen/2024/*.pdf")
data = []

def get_pages(filename):
    raw_xml = parser.from_file(filename, xmlContent=True)
    body = raw_xml['content'].split('<body>')[1].split('</body>')[0]
    body_without_tag = body.replace("<p>", "").replace("</p>", "").replace("<div>", "").replace("</div>","").replace("<p />","")
    text_pages = body_without_tag.split("""<div class="page">""")[1:]
    num_pages = len(text_pages)
    if not num_pages==int(raw_xml['metadata']['xmpTPg:NPages']) : #check if it worked correctly
        print("ERROR in page number crosscheck")
        exit(1)
    return text_pages


def parse_float(float_str_eu: str):
    return float(float_str_eu.replace(".", "").replace(",","."))

@dataclass
class Page:
    month_year: str = field()
    name: str = field()
    arbeitsmarktzulage: float = field()
    muenchenzulage: float = field()
    is_rueckrechnung: bool = field()

    def __init__(self, page: str):
        # Initialize fields with default values
        self._lines = page.split('\n')


        self.month_year = self.line_with("Gehaltsabrechnung").split(" ")[-1]

        self.name = self.line_with(" Abteilung").split(" Abteilung")[0]

        self.is_rueckrechnung = "Rückrechnung" in page

        index_start = self.line_index_with("Kosten- Kosten- Lohn") 
        index_end = self.line_index_with("GESAMTBRUTTO")
        lines_loehne = self._lines[index_start+3: index_end-1]

        self.arbeitsmarktzulage = parse_float(self.line_with("Arbeitsmarktzulage").split(" ")[2]) if "Arbeitsmarktzulage" in "".join(lines_loehne) else 0
        self.muenchenzulage = parse_float(self.line_with("Münchenzulage").split(" ")[2]) if "Münchenzulage" in "".join(lines_loehne) else 0

        print("---")
        print("\n".join(lines_loehne))
        print("---")

    def line_with(self, text: str):
        return [line for line in self._lines if text in line][0]

    def line_index_with(self, text: str):
        return [index for index, line in enumerate(self._lines) if text in line][0]

pages = []
for pdf in pdfs:
    print(f"Reading {pdf}...")
    text_pages = get_pages(pdf)
    for page in text_pages:
        page_obj = Page(page)
        print(page_obj)
        pages.append(page_obj)
