from pandas.core.arrays import boolean
from tika import parser
from pandas import DataFrame, ExcelWriter
import glob, re, os

YEAR = "2025"
MON = "AUGUST"
pdfs = glob.glob(f"ag_belastung/{YEAR}/August.pdf")
data = []

HEADER_END = "Pers.Nr. Einheiten"
FOOTER_START = "Lohnservice Wendel eG"


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


if len(pdfs) != 1:
    raise OSError("expected one pdf")


def line_with(lines: list, text: str):
    return [line for line in lines if text in line][0]


def line_index_with(lines: list, text: str):
    return [index for index, line in enumerate(lines) if text in line][0]


pages = get_pages(pdfs[0])

lines = []
for page in pages:
    pLines = page.split("\n")
    index_start = line_index_with(pLines, HEADER_END)
    index_end = line_index_with(pLines, FOOTER_START)
    lines.extend(
        [line for line in pLines[index_start + 1 : index_end] if line.strip() != ""]
    )

GESAMTBRUTTO = "Brutto (Gesamt)"
MONATSBRUTTO = "Brutto (Monat)"
SV_AG_GESAMT = "SV-AG (Gesamt)"
SV_AG_MONAT = "SV-AG (Monat)"
U1_GESAMT = "U1 (Gesamt)"
U1_MONAT = "U1 (Monat)"
U2_GESAMT = "U2 (Gesamt)"
U2_MONAT = "U2 (Monat)"


def process_entry(
    data,
    nextLineRR,
    lineSplit: list,
    nextLineSplit: list,
    monat_header: str,
    gesamt_header: str,
    plus: bool,
):
    sign = 1.0 if plus else -1.0
    gesamt = 0.0
    monat = 0.0
    if nextLineRR:
        print(f"Processing also '{' '.join(nextLineSplit)}'")
        gesamt = sign * parse_float(nextLineSplit[-1])
        monat = sign * (parse_float(nextLineSplit[-2]) + parse_float(lineSplit[-1]))
    else:
        has_monthly = re.match(r"^-{0,1}\d+\.{0,1}\d*\,\d{2}", lineSplit[-2]) != None
        gesamt = sign * parse_float(lineSplit[-1])
        monat = sign * parse_float(lineSplit[-2]) if has_monthly else 0.0
    data[current_employee][gesamt_header] += gesamt
    data[current_employee][monat_header] += monat
    print(f">{gesamt_header}+={gesamt}, {monat_header}+={monat}")
    return nextLineRR


data = {}
current_employee = ""
current_employee_done = False
RR_line_processed = False
for idx, line in enumerate(lines):
    lineSplit = line.split(" ")
    nextLineSplit = lines[idx + 1].split(" ") if idx < len(lines) - 1 else []
    nextLineRR = (
        re.match(r"^aus RR: -{0,1}\d+\.{0,1}\d*\,\d{2}", lines[idx + 1])
        if idx < len(lines) - 1
        else False
    )
    if RR_line_processed:
        RR_line_processed = False
        continue
    print(f"Processing '{line}'")
    if re.match(r"^\d", line):
        has_two_values = re.match(r"^-{0,1}\d+\.{0,1}\d*\,\d{2}", lineSplit[-2]) != None
        current_employee = " ".join(lineSplit[1 : (-2 if has_two_values else -1)])
        current_employee_done = False
        data[current_employee] = {
            GESAMTBRUTTO: 0.0,
            MONATSBRUTTO: 0.0,
            SV_AG_GESAMT: 0.0,
            SV_AG_MONAT: 0.0,
            U1_GESAMT: 0.0,
            U1_MONAT: 0.0,
            U2_GESAMT: 0.0,
            U2_MONAT: 0.0,
        }
        print(f"--- BEGIN {current_employee} ---")
        RR_line_processed = process_entry(
            data, nextLineRR, lineSplit, nextLineSplit, MONATSBRUTTO, GESAMTBRUTTO, True
        )
        continue
    if line.startswith("Zwischensummen"):
        current_employee_done = True
        print(f">data: {data[current_employee]}")
        print(f"--- END {current_employee} ---\n")
    if current_employee_done:
        continue
    if (
        line.startswith("SV-AG Anteil (Pflicht)")
        or line.startswith("SV-AG Anteil (Pauschal)")
        or line.startswith("Umlage 1/2")
        or line.startswith("Insolvenzgeldumlage")
        or line.startswith("aus RR: Umlage 1/2")
        or line.startswith("aus RR: SV-AG Anteil (Pflicht)")
        or line.startswith("aus RR: Insolvenzgeldumlage")
        or line.startswith("geringf. p. Steuer")
    ):
        RR_line_processed = process_entry(
            data, nextLineRR, lineSplit, nextLineSplit, SV_AG_MONAT, SV_AG_GESAMT, True
        )
        continue
    if line.startswith("Erst. Entg. AU") or line.startswith("aus RR: Erst. Entg. AU"):
        RR_line_processed = process_entry(
            data, nextLineRR, lineSplit, nextLineSplit, U1_MONAT, U1_GESAMT, False
        )
        continue
    if (
        line.startswith("Erst. Entg. B.Verbot")
        or line.startswith("aus RR: Erst. Entg. B.Verbot")
        or line.startswith("Erst. SV-AG B.Verbot")
        or line.startswith("aus RR: Erst. SV-AG B.Verbot")
        or line.startswith("Erst. Mutterschutz")
        or line.startswith("aus RR: Erst. Mutterschutz")
    ):
        RR_line_processed = process_entry(
            data, nextLineRR, lineSplit, nextLineSplit, U2_MONAT, U2_GESAMT, False
        )
        continue

    raise OSError(f"Unable to process unknown line {line}")
print("Finished reading")

OUT_FILENAME = f"ag_belastung_{YEAR}_{MON}.xlsx"
print(f"\nCreating {OUT_FILENAME}")
if os.path.exists(OUT_FILENAME):
    os.remove(OUT_FILENAME)

TITLE = "AG Belastung"
with ExcelWriter(OUT_FILENAME, engine="openpyxl", mode="w") as writer:
    df = DataFrame.from_dict(data, orient="columns").T
    order = [
        MONATSBRUTTO,
        SV_AG_MONAT,
        U1_MONAT,
        U2_MONAT,
        GESAMTBRUTTO,
        SV_AG_GESAMT,
        U1_GESAMT,
        U2_GESAMT,
    ]
    df = df[order]
    title_df = DataFrame([{"title": TITLE}])
    title_df.to_excel(writer, sheet_name=TITLE, index=False, header=False, startrow=0)
    df.to_excel(writer, sheet_name=TITLE, index=True, header=True, startrow=2)
    writer.sheets[TITLE].column_dimensions["A"].width = 30
    for column in ["B", "C", "D", "E", "F", "G", "H", "I"]:
        writer.sheets[TITLE].column_dimensions[column].width = 15
print("done")
