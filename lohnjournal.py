from pandas.core.arrays import boolean
from pypdf import PdfReader
from pandas import DataFrame, ExcelWriter
import datetime
import glob, re, os

YEAR = str(datetime.date.today().year)

HEADER_END = "Name E Kl"
FOOTER_START = "Negative Werte sind"
END_TEXT = "Summen: "


def get_pages(filename):
    reader = PdfReader(filename)
    return [page.extract_text() or "" for page in reader.pages]


def parse_float(float_str_eu: str):
    normalized = re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹]+\)?$", "", float_str_eu.strip())
    return float(normalized.replace(".", "").replace(",", "."))


def unique(lst: list):
    seen = set()
    seen_add = seen.add
    return [x for x in lst if not (x in seen or seen_add(x))]


def line_with(lines: list, text: str):
    return [line for line in lines if text in line][0]


def line_index_with(lines: list, text: str):
    return [index for index, line in enumerate(lines) if text in line][0]


def process(pdf_paths, year=YEAR, output_path=None):
    if len(pdf_paths) != 1:
        raise OSError("expected one pdf")

    print(f"Lese PDF: {pdf_paths[0]}")
    pages = get_pages(pdf_paths[0])
    print(f"  {len(pages)} Seite(n) gefunden, extrahiere Zeilen...")

    lines = []
    for page in pages:
        pLines = page.split("\n")
        index_start = line_index_with(pLines, HEADER_END)
        index_end = line_index_with(pLines, FOOTER_START)
        lines.extend(
            [line for line in pLines[index_start + 1 : index_end] if line.strip() != ""]
        )
    
    print(f"Starte Verarbeitung von {len(lines)} Zeile(n)")
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
        gesamtbrutto = parse_float(line_split[7]) if len(line_split) >= 8 else 0.0
        steuerbrutto = parse_float(line_split[8]) if len(line_split) >= 9 else 0.0
        i += 1
        line_split = re.split(r"(\b\d{1,3}(?:\.\d{3})*,\d+\b)", lines[i], maxsplit=1)
        name = line_split[0].strip().strip(" *)")
        if not re.match(r"^\d{6}", lines[i + 1]) and not "Summen" in lines[i + 1]:
            print(f"FEHLER: nicht erwartetes format für {name}")
            data[name] = {STEUERBRUTTO: None, GESAMTBRUTTO: None, SV_AG: None}
            i += 2
            continue
        sv_ag = parse_float(line_split[1]) if len(line_split) > 1 else 0.0
        if name in data:
            print(
                f"WARNUNG: Zwei Lohnjournal Seiten für {name} - addiere Werte - Kontrolle!"
            )
            existing = data[name]
            steuerbrutto = (existing[STEUERBRUTTO] or 0.0) + steuerbrutto
            gesamtbrutto = (existing[GESAMTBRUTTO] or 0.0) + gesamtbrutto
            sv_ag = (existing[SV_AG] or 0.0) + sv_ag
        data[name] = {
            STEUERBRUTTO: steuerbrutto,
            GESAMTBRUTTO: gesamtbrutto,
            SV_AG: sv_ag,
        }
    print(f"Verarbeitung abgeschlossen: {len(data)} Mitarbeiter ausgewertet")
    
    OUT_FILENAME = output_path or f"lohnjournal_{year}.xlsx"
    print(f"\nErstelle {OUT_FILENAME}")
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
        for row in writer.sheets[TITLE].iter_rows(min_row=4, min_col=2, max_col=4):
            for cell in row:
                if isinstance(cell.value, (int, float)):
                    cell.number_format = "#,##0.00"
        for column in ["B", "C", "D", "E", "F", "G", "H", "I"]:
            writer.sheets[TITLE].column_dimensions[column].width = 15
    print("fertig")
    return OUT_FILENAME


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(
        description=(
            "Verarbeitet das Lohnjournal-PDF (Dezember-Ausdruck) und schreibt das Ergebnis in eine Excel-Datei.\n\n"
            "Erwartete Datei:\n"
            "  lohnjournal/12.<YEAR>.pdf\n\n"
            "Aus dem PDF werden Steuerbrutto, Gesamtbrutto und SV-AG-Anteil je Mitarbeiter extrahiert."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--year", default=YEAR,
        help=f"Abrechnungsjahr (Standard: {YEAR})",
    )
    args = ap.parse_args()
    pdfs = glob.glob(f"lohnjournal/12.{args.year}.pdf")
    if not pdfs:
        print(f"Keine PDF gefunden: lohnjournal/12.{args.year}.pdf")
        exit(1)
    print(f"PDF gefunden: {pdfs[0]}")
    process(pdfs, year=args.year)
