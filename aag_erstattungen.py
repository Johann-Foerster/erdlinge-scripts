from tika import parser
from openpyxl import Workbook
import datetime
import glob, os

YEAR = str(datetime.date.today().year)
ROW_SUM = "Summe"


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
        raise RuntimeError("FEHLER beim Abgleich der Seitenanzahl")
    return text_pages


def find_index(data, element):
    for index, item in enumerate(data):
        if item == element:
            return index
    return -1


def process(pdf_paths, year=YEAR, output_path=None):
    erstattungen_u1 = {}
    erstattungen_u2 = {}

    print(f"Starte Verarbeitung von {len(pdf_paths)} PDF-Datei(en)...")
    for pdf in pdf_paths:
        print(f"Lese PDF: {pdf}")
        text_pages = get_pages(pdf)
        print(f"  {len(text_pages)} Seite(n) gefunden, werte aus...")
        for page in text_pages:
            if "Rückrechnung" in page:
                continue
            lines = page.split("\n")

            vorname = " ".join(
                [
                    lines[idx + 2]
                    for idx, line in enumerate(lines)
                    if "Vorname Rentenversicherungsnummer" in line
                ][0].split(" ")[:-1]
            )
            nachname = " ".join(
                [
                    lines[idx + 2]
                    for idx, line in enumerate(lines)
                    if "Name Pers.Nr." in line
                ][0].split(" ")[:-1]
            )
            name = f"{vorname} {nachname}"

            type = (
                "U1"
                if "Arbeitsunfähigkeit - U1" in page
                else (
                    "U2"
                    if "Mutterschaft - U2" in page or "Beschäftigungsverbot - U2" in page
                    else "TYPE ERROR"
                )
            )
            if type == "TYPE ERROR":
                raise OSError(
                    f"Konnte Seitentyp (U1/U2) nicht bestimmen (Datei: {pdf}). Bitte PDF prüfen."
                )
            value = ""
            if "Mutterschaft - U2" in page:
                value = [line for line in lines if " im Monat " in line][0].split(
                    " im Monat "
                )[1]
            else:
                value = " ".join(
                    [line for line in lines if "Summe Erstattungsbetrag" in line][0].split(
                        " "
                    )[2:]
                )
            value_eur = float(value.replace(" €", "").replace(".", "").replace(",", "."))

            if "X Stornierung" in page:
                value_eur = -value_eur
            title = pdf.split("/")[-1].replace(".pdf", "")

            if type == "U1":
                if name not in erstattungen_u1:
                    erstattungen_u1[name] = {}
                erstattungen_u1[name][title] = (
                    erstattungen_u1[name][title] + value_eur
                    if title in erstattungen_u1[name]
                    else value_eur
                )
            else:
                if name not in erstattungen_u2:
                    erstattungen_u2[name] = {}
                erstattungen_u2[name][title] = (
                    erstattungen_u2[name][title] + value_eur
                    if title in erstattungen_u2[name]
                    else value_eur
                )

    # summing up
    print(
        f"Bilde Summen: {len(erstattungen_u1)} Mitarbeiter (U1), "
        f"{len(erstattungen_u2)} Mitarbeiter (U2)"
    )
    for name in erstattungen_u1.keys():
        erstattungen_u1[name][ROW_SUM] = sum(erstattungen_u1[name].values())
    for name in erstattungen_u2.keys():
        erstattungen_u2[name][ROW_SUM] = sum(erstattungen_u2[name].values())

    titles = [x.split("/")[-1].replace(".pdf", "") for x in pdf_paths]
    outfile = output_path or f"AAG_Erstattungen_{year}.xlsx"
    print(f"\nSchreibe Excel-Datei: {outfile}")

    wb = Workbook()
    ws = wb.active
    ws.title = "AAG Erstattungen"

    def schreibe_block(typ, erstattungen):
        ws.append([typ])
        ws.append(["Name"] + titles + [ROW_SUM])
        for name in erstattungen.keys():
            ws.append(
                [name]
                + [
                    (erstattungen[name][x] if x in erstattungen[name] else 0)
                    for x in titles
                ]
                + [erstattungen[name][ROW_SUM]]
            )

    schreibe_block("U1", erstattungen_u1)
    ws.append([])
    schreibe_block("U2", erstattungen_u2)

    ws.column_dimensions["A"].width = 30
    for row in ws.iter_rows(min_col=2):
        for cell in row:
            if isinstance(cell.value, (int, float)):
                cell.number_format = "#,##0.00"

    wb.save(outfile)
    print("...fertig geschrieben!")
    return outfile


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(
        description=(
            "Verarbeitet AAG-Erstattungs-PDFs (U1 und U2) und schreibt das Ergebnis in eine Excel-Datei.\n\n"
            "Erwartete Ordnerstruktur:\n"
            "  aag_erstattungen/<YEAR>/*.pdf\n\n"
            "Jede PDF-Seite wird als U1 (Arbeitsunfähigkeit) oder U2 (Mutterschaft/Beschäftigungsverbot)\n"
            "klassifiziert und der Erstattungsbetrag je Mitarbeiter summiert."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--year", default=YEAR,
        help=f"Abrechnungsjahr (Standard: {YEAR})",
    )
    args = ap.parse_args()
    pdfs = glob.glob(f"aag_erstattungen/{args.year}/*.pdf")
    if not pdfs:
        print(f"Keine PDFs gefunden in: aag_erstattungen/{args.year}/")
        exit(1)
    print(f"{len(pdfs)} PDF(s) gefunden in: aag_erstattungen/{args.year}/")
    process(pdfs, year=args.year)
