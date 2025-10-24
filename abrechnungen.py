from enum import unique
from tika import parser
from dataclasses import dataclass, field
from collections import OrderedDict
from pandas import DataFrame, ExcelWriter
import numpy as np
import glob, os, re

YEAR = "2025"
pdfs = glob.glob(f"abrechnungen/{YEAR}/*.pdf")
data = []

AMZ = "Arbeitsmarktzulage"
MZ = "Münchenzulage"
FKZ = "Fahrten zw."
EUW = "Entgeltumw.Altersv.lfd"
MUT = "Mutterschaftsgeld"
MUTF = "Mutterschutzfrist"
BV = "Beschäftigungsverbot"
WAZ = "Arb.Zeit"
TVOD = "TVöD SuE Arbeitnehmer Grundvergütung"


def get_pages(filename):
    raw_xml = parser.from_file(filename, xmlContent=True)
    body = raw_xml["content"].split("<body>")[1].split("</body>")[0]
    body_without_tag = (
        body.replace("<p>", "")
        .replace("</p>", "")
        .replace("<div>", "")
        .replace("</div>", "")
        .replace("<p />", "")
    )
    text_pages = body_without_tag.split("""<div class="page">""")[1:]
    num_pages = len(text_pages)
    if not num_pages == int(
        raw_xml["metadata"]["xmpTPg:NPages"]
    ):  # check if it worked correctly
        print("ERROR in page number crosscheck")
        exit(1)
    return text_pages


def parse_float(float_str_eu: str):
    return float(float_str_eu.replace(".", "").replace(",", "."))


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
    wochenarbeitszeit: float = field()
    gruppe_stufe: str = field()

    def __init__(self, page: str):
        # Initialize fields with default values
        self._page = page
        self._lines = page.split("\n")

        self.month_year = self.line_with("Gehaltsabrechnung").split(" ")[-1]
        self.month = int(self.month_year.split(".")[0])

        self.name = self.line_with(" Abteilung").split(" Abteilung")[0]

        self.is_rueckrechnung = "Rückrechnung" in page

        index_start = self.line_index_with("Kosten- Kosten- Lohn")
        index_end = self.line_index_with("GESAMTBRUTTO")
        lines_loehne = [
            line
            for line in self._lines[index_start + 2 : index_end]
            if line.strip() != ""
        ]

        self.arbeitsmarktzulage = (
            parse_float(self.line_with(AMZ).split(" ")[2])
            if AMZ in "".join(lines_loehne)
            else 0
        )

        self.muenchenzulage = (
            parse_float(self.line_with(MZ).split(" ")[2])
            if MZ in "".join(lines_loehne)
            else 0
        )

        self.gruppe_stufe = (
            self.gruppe_stufe(self.line_with(TVOD)) if TVOD in page else "-"
        )

        self.fahrtkostenzuschuss = (
            parse_float(self.line_with(FKZ).split(" ")[7]) if FKZ in page else 0
        )

        WAZ_HEAD_IDX = self._lines.index(self.line_with(WAZ))
        WAZ_LINE = self._lines[WAZ_HEAD_IDX + 3]
        WAZ_MATCH = re.search(
            r"(\d+,\d+)(?= \d+,\d+)", " ".join(WAZ_LINE.split(" ")[1:])
        )
        self.wochenarbeitszeit = parse_float(WAZ_MATCH.group(0)) if WAZ_MATCH else -1

        steuerfrei_lines = [line for line in lines_loehne if not line.endswith("* *")]
        steuerfrei_values = [
            parse_float(line.split(" *")[0].split(" ")[-1]) for line in steuerfrei_lines
        ]

        # Entgeldumwandlung during Beschäftigungsverbot and not when Mutterschutzfrist started
        steuerfrei_entgeltumw = (
            -parse_float(self.line_with(EUW).split(" ")[-1]) if EUW in page else 0
        )
        if EUW in page and MUT in page:
            fehlzeit_start = self.line_with(MUTF).split(" ")[1]
            if (
                int(fehlzeit_start.split(".")[0]) == 1
                or int(fehlzeit_start.split(".")[1]) < self.month
            ):
                print(
                    f"For {self.name} {MUTF} started {fehlzeit_start} so in month {self.month} there is no unversteuert {EUW}"
                )
                steuerfrei_entgeltumw = 0

        self.steuerfrei_inkl_fahrtkostenzuschuss = (
            self.fahrtkostenzuschuss + sum(steuerfrei_values) + steuerfrei_entgeltumw
        )

    def line_with(self, text: str):
        return [line for line in self._lines if text in line][0]

    def line_index_with(self, text: str):
        return [index for index, line in enumerate(self._lines) if text in line][0]

    def gruppe_stufe(self, line: str):
        parts = line.split("Grundvergütung")[-1].strip().split(" ")
        return (
            f"S{parts[1]}/{parts[3]}" if parts[0] == "S" else f"{parts[0]}/{parts[2]}"
        )


pages = []
for pdf in pdfs:
    print(f"Reading {pdf}...")
    text_pages = get_pages(pdf)
    for tpage in text_pages:
        page_obj = Page(tpage)
        if YEAR not in page_obj.month_year:
            print(
                f"Skipping page not for year {YEAR} (RR={page_obj.is_rueckrechnung}): {page_obj}"
            )
            continue
        pages.append(page_obj)

months = unique([page.month for page in pages])
names = unique([page.name for page in pages])

tables = [
    {"name": "Arbeitsmarktzulage", "field": "arbeitsmarktzulage"},
    {"name": "Münchenzulage", "field": "muenchenzulage"},
    {"name": "Fahrtkostenzuschuss", "field": "fahrtkostenzuschuss"},
    {
        "name": "Steuerfrei (inkl. FKZ)",
        "field": "steuerfrei_inkl_fahrtkostenzuschuss",
    },
    {"name": "Wochenarbeitszeit", "field": "wochenarbeitszeit"},
    {"name": "Gehaltsgruppe-Stufe", "field": "gruppe_stufe"},
]
print(
    f"\nCreating tables {[table['name'] for table in tables]} for months {months} and employees {names}"
)

data = {}
for name in names:
    employee_pages = [page for page in pages if page.name in name]
    for page in employee_pages:
        if page.month not in data:
            data[page.month] = {}
        if name not in data[page.month]:
            data[page.month][page.name] = {}
        for table in tables:
            datapoint = getattr(page, table["field"])
            if table["name"] in data[page.month][page.name]:
                old_datapoint = data[page.month][page.name][table["name"]]
                if old_datapoint != datapoint:
                    print(
                        f"Changed {table['name']} for {page.name}, month {page.month}, old={old_datapoint}, new={datapoint}, RR={page.is_rueckrechnung} page={page}"
                    )
            data[page.month][page.name][table["name"]] = datapoint

OUT_FILENAME = f"abrechnungen_{YEAR}.xlsx"
print(f"\nCreating {OUT_FILENAME}")
if os.path.exists(OUT_FILENAME):
    os.remove(OUT_FILENAME)

with ExcelWriter(OUT_FILENAME, engine="openpyxl", mode="w") as writer:
    for table in tables:
        df = DataFrame()
        for month in months:
            for employee in names:
                df.loc[employee, month] = (
                    data[month][employee][table["name"]]
                    if employee in data[month]
                    else 0
                )
        if np.issubdtype(df.dtypes.values[0], np.number):
            df["Summe"] = df.sum(axis=1)
        title_df = DataFrame([{"Daten": table["name"]}])
        title_df.to_excel(
            writer, sheet_name=table["name"], index=False, header=False, startrow=0
        )
        df.to_excel(
            writer, sheet_name=table["name"], index=True, header=True, startrow=2
        )
        writer.sheets[table["name"]].column_dimensions["A"].width = 30
print("done")
