import csv
from datetime import datetime
from collections import defaultdict
from openpyxl import load_workbook, Workbook
from openpyxl.styles import PatternFill, Font, Alignment


def lese_gls_konto(pfad):
    """Liest GLS_Konto.csv und gibt Liste von (datum, betrag, betreff) zurück."""
    buchungen = []
    with open(pfad, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            buchungstag = datetime.strptime(row["Buchungstag"], "%d.%m.%Y").date()
            valutadatum = datetime.strptime(row["Valutadatum"], "%d.%m.%Y").date()
            datum = min(buchungstag, valutadatum)
            betrag_str = row["Betrag"].replace(".", "").replace(",", ".")
            betrag = round(float(betrag_str), 2)
            betreff = row["Verwendungszweck"]
            buchungen.append((datum, betrag, betreff))
    return buchungen


def lese_gls_buchhaltung(pfad):
    """Liest GLS_Buchhaltung.xlsx und gibt Liste von (datum, betrag, betreff) zurück."""
    buchungen = []
    wb = load_workbook(pfad)
    ws = wb.active
    headers = [cell.value for cell in ws[1]]
    idx_datum = headers.index("Datum")
    idx_text = headers.index("Buchungstext")
    idx_soll = headers.index("Gutschrift / Soll")
    idx_haben = headers.index("Lastschrift / Haben")

    for row in ws.iter_rows(min_row=2, values_only=True):
        datum_val = row[idx_datum]
        if datum_val is None:
            continue  # z.B. Anfangssaldo-Zeile
        if isinstance(datum_val, datetime):
            datum = datum_val.date()
        else:
            continue

        soll = row[idx_soll]  # Gutschrift = positiv
        haben = row[idx_haben]  # Lastschrift = negativ

        if soll is not None:
            betrag = round(float(soll), 2)
        elif haben is not None:
            betrag = round(-float(haben), 2)
        else:
            continue

        betreff = row[idx_text] or ""
        buchungen.append((datum, betrag, betreff))
    return buchungen


def abgleich(gls_buchungen, bh_buchungen):
    """Matcht Buchungen anhand (Datum, Betrag). Gibt drei Listen zurück."""

    # Gruppiere nach (datum, betrag) -> Liste von Betreffen
    gls_map = defaultdict(list)
    for datum, betrag, betreff in gls_buchungen:
        gls_map[(datum, betrag)].append(betreff)

    bh_map = defaultdict(list)
    for datum, betrag, betreff in bh_buchungen:
        bh_map[(datum, betrag)].append(betreff)

    alle_keys = set(gls_map.keys()) | set(bh_map.keys())

    uebereinstimmend = []
    nur_gls = []
    nur_bh = []

    for key in sorted(alle_keys):
        datum, betrag = key
        gls_liste = gls_map.get(key, [])
        bh_liste = bh_map.get(key, [])

        # Matche paarweise so viele wie möglich
        anzahl_match = min(len(gls_liste), len(bh_liste))

        for i in range(anzahl_match):
            uebereinstimmend.append((datum, betrag, gls_liste[i], bh_liste[i]))

        # Überschüssige GLS-Buchungen
        for i in range(anzahl_match, len(gls_liste)):
            nur_gls.append((datum, betrag, gls_liste[i], ""))

        # Überschüssige Buchhaltungs-Buchungen
        for i in range(anzahl_match, len(bh_liste)):
            nur_bh.append((datum, betrag, "", bh_liste[i]))

    return nur_gls, nur_bh, uebereinstimmend


def schreibe_ergebnis(pfad, nur_gls, nur_bh, uebereinstimmend):
    """Schreibt das Ergebnis in eine xlsx-Datei."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Kontoabgleich GLS"

    # Header
    headers = ["Datum", "Betrag", "Betreff GLS", "Betreff Buchhaltung", "Status"]
    ws.append(headers)

    # Header-Formatierung
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    # Farben für Status
    fill_nur_gls = PatternFill(start_color="FCE4EC", end_color="FCE4EC", fill_type="solid")
    fill_nur_bh = PatternFill(start_color="FFF3E0", end_color="FFF3E0", fill_type="solid")
    fill_ok = PatternFill(start_color="E8F5E9", end_color="E8F5E9", fill_type="solid")

    def schreibe_block(daten, status, fill):
        for datum, betrag, betreff_gls, betreff_bh in daten:
            ws.append([datum, betrag, betreff_gls, betreff_bh, status])
            for cell in ws[ws.max_row]:
                cell.fill = fill

    schreibe_block(nur_gls, "nur GLS", fill_nur_gls)
    schreibe_block(nur_bh, "nur Buchhaltung", fill_nur_bh)
    schreibe_block(uebereinstimmend, "übereinstimmend", fill_ok)

    # Spaltenbreiten
    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 60
    ws.column_dimensions["D"].width = 60
    ws.column_dimensions["E"].width = 20

    # Betrag als Zahl formatieren
    for row in ws.iter_rows(min_row=2, min_col=2, max_col=2):
        for cell in row:
            cell.number_format = '#,##0.00'

    # Datum formatieren
    for row in ws.iter_rows(min_row=2, min_col=1, max_col=1):
        for cell in row:
            cell.number_format = 'DD.MM.YYYY'

    wb.save(pfad)


def main():
    gls_buchungen = lese_gls_konto("kontoabgleich/GLS_Konto.csv")
    bh_buchungen = lese_gls_buchhaltung("kontoabgleich/GLS_Buchhaltung.xlsx")

    print(f"GLS Konto: {len(gls_buchungen)} Buchungen")
    print(f"Buchhaltung: {len(bh_buchungen)} Buchungen")

    nur_gls, nur_bh, uebereinstimmend = abgleich(gls_buchungen, bh_buchungen)

    print(f"\nErgebnis:")
    print(f"  Übereinstimmend:  {len(uebereinstimmend)}")
    print(f"  Nur GLS:          {len(nur_gls)}")
    print(f"  Nur Buchhaltung:  {len(nur_bh)}")

    schreibe_ergebnis("kontoabgleich/kontoabgleich_gls.xlsx", nur_gls, nur_bh, uebereinstimmend)
    print("\nDatei geschrieben: kontoabgleich/kontoabgleich_gls.xlsx")


if __name__ == "__main__":
    main()
