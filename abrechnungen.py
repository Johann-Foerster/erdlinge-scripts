from enum import unique
from tika import parser
from dataclasses import dataclass, field
from collections import OrderedDict
import glob

YEAR = "2024"
pdfs = glob.glob(f"abrechnungen/{YEAR}/*.pdf")
data = []

AMZ = "Arbeitsmarktzulage"
MZ  = "Münchenzulage"
FKZ = "Fahrten zw."

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

def unique(lst: list):
    seen = set()
    seen_add = seen.add
    return [x for x in lst if not (x in seen or seen_add(x))]

@dataclass
class Page:
    month_year: str = field()
    month: int = field()
    name: str = field()
    arbeitsmarktzulage: float = field()
    muenchenzulage: float = field()
    fahrtkostenzuschuss: float = field()
    steuerfrei_inkl_fahrtkostenzuschuss: float = field()
    is_rueckrechnung: bool = field()

    def __init__(self, page: str):
        # Initialize fields with default values
        self._page = page
        self._lines = page.split('\n')


        self.month_year = self.line_with("Gehaltsabrechnung").split(" ")[-1]
        self.month = int(self.month_year.split(".")[0])

        self.name = self.line_with(" Abteilung").split(" Abteilung")[0]

        self.is_rueckrechnung = "Rückrechnung" in page

        index_start = self.line_index_with("Kosten- Kosten- Lohn") 
        index_end = self.line_index_with("GESAMTBRUTTO")
        lines_loehne = [line for line in self._lines[index_start+2: index_end] if line.strip() != ""]

        self.arbeitsmarktzulage = parse_float(self.line_with(AMZ).split(" ")[2]) if AMZ in "".join(lines_loehne) else 0
        
        self.muenchenzulage = parse_float(self.line_with(MZ).split(" ")[2]) if MZ in "".join(lines_loehne) else 0
        
        self.fahrtkostenzuschuss = parse_float(self.line_with(FKZ).split(" ")[7]) if FKZ in page else 0

        steuerfrei_lines = [line for line in lines_loehne if not line.endswith("* *")]
        steuerfrei_values = [parse_float(line.split(" *")[0].split(" ")[-1]) for line in steuerfrei_lines]
        self.steuerfrei_inkl_fahrtkostenzuschuss = self.fahrtkostenzuschuss + sum(steuerfrei_values)

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
        if not (YEAR in page_obj.month_year):
            print(f"Skipping page not for year {YEAR} (Rückrechung={page_obj.is_rueckrechnung}): {page_obj}")
            continue
        pages.append(page_obj)

months = unique([page.month for page in pages])
names = unique([page.name for page in pages])

print(f"Creating table for months {months} and employees {names}")

