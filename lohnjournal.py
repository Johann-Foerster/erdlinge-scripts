from pandas.core.arrays import boolean
from tika import parser
from pandas import DataFrame, ExcelWriter
import glob, re, os

YEAR = "2024"
pdfs = glob.glob(f"lohnjournal/12.2024.pdf")
data = []

HEADER_END = "Name E Kl"
FOOTER_START = "Negative Werte sind"
END_TEXT = "Summen: "


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

print("Start processing")
i = 0
data = {}
STEUERBRUTTO = "Steuerbrutto"
GESAMTBRUTTO = "Gesamtbrutto"
SV_AG = "SV-AG Anteil"
while i < len(lines):
    line_split = lines[i].split(" ")
    if not re.match(r"^\d{6}$", line_split[0]):
        i += 1
        continue
    gesamtbrutto = line_split[7] if len(line_split) >= 8 else "0"
    steuerbrutto = line_split[8] if len(line_split) >= 9 else "0"
    i += 1
    line_split = re.split(r"(\b\d{1,3}(?:\.\d{3})*,\d+\b)", lines[i], maxsplit=1)
    name = line_split[0].strip().strip(" *)")
    if not re.match(r"^\d{6}", lines[i + 1]) and not "Summen" in lines[i + 1]:
        print(f"FEHLER: nicht erwartetes format für {name}")
        data[name] = {STEUERBRUTTO: "?", GESAMTBRUTTO: "?", SV_AG: "?"}
        i += 2
        continue
    sv_ag = line_split[1] if len(line_split) > 1 else "0"
    if name in data:
        print(
            f"WARNUNG: Zwei Lohnjournal Seiten für {name} - addiere Werte - Kontrolle!"
        )
        steuerbrutto = (
            f"{(parse_float(data[name][STEUERBRUTTO]) + parse_float(steuerbrutto)):.2f}"
        )
        gesamtbrutto = (
            f"{(parse_float(data[name][GESAMTBRUTTO]) + parse_float(gesamtbrutto)):.2f}"
        )
        sv_ag = f"{(parse_float(data[name][SV_AG]) + parse_float(sv_ag)):.2f}"
    data[name] = {
        STEUERBRUTTO: steuerbrutto,
        GESAMTBRUTTO: gesamtbrutto,
        SV_AG: sv_ag,
    }
print("Finished processing")

OUT_FILENAME = f"lohnjournal_{YEAR}.xlsx"
print(f"\nCreating {OUT_FILENAME}")
if os.path.exists(OUT_FILENAME):
    os.remove(OUT_FILENAME)

TITLE = "Lohnjournal"
with ExcelWriter(OUT_FILENAME, engine="openpyxl", mode="w") as writer:
    df = DataFrame.from_dict(data, orient="columns").T
    order = [STEUERBRUTTO, GESAMTBRUTTO, SV_AG]
    df = df[order]
    title_df = DataFrame([{"title": TITLE}])
    title_df.to_excel(writer, sheet_name=TITLE, index=False, header=False, startrow=0)
    df.to_excel(writer, sheet_name=TITLE, index=True, header=True, startrow=2)
    writer.sheets[TITLE].column_dimensions["A"].width = 30
    for column in ["B", "C", "D", "E", "F", "G", "H", "I"]:
        writer.sheets[TITLE].column_dimensions[column].width = 15
print("done")
