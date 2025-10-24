"""
Core processing functions for different document types.
These functions contain the main logic extracted from the CLI scripts.
"""
from enum import unique
from tika import parser
from dataclasses import dataclass, field
from collections import OrderedDict
from pandas import DataFrame, ExcelWriter
import numpy as np
import glob, os, re, csv
import io
import tempfile


def parse_float(float_str_eu: str):
    """Parse European-style float string to Python float."""
    return float(float_str_eu.replace(".", "").replace(",", "."))


def unique(lst: list):
    """Return unique items from list while preserving order."""
    seen = set()
    seen_add = seen.add
    return [x for x in lst if not (x in seen or seen_add(x))]


def get_pages(file_content: bytes, filename: str = "temp.pdf"):
    """Extract pages from PDF content using tika parser."""
    # Save content to temporary file for tika processing
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        temp_file.write(file_content)
        temp_filename = temp_file.name
    
    try:
        raw_xml = parser.from_file(temp_filename, xmlContent=True)
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
            return []
        return text_pages
    finally:
        # Clean up temporary file
        os.unlink(temp_filename)


# Abrechnungen (Payroll) Processing
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
        # Constants
        AMZ = "Arbeitsmarktzulage"
        MZ = "Münchenzulage"
        FKZ = "Fahrten zw."
        EUW = "Entgeltumw.Altersv.lfd"
        MUT = "Mutterschaftsgeld"
        MUTF = "Mutterschutzfrist"
        BV = "Beschäftigungsverbot"
        WAZ = "Arb.Zeit"
        TVOD = "TVöD"
        
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
            self.gruppe_stufe_func(self.line_with(TVOD)) if TVOD in page else "-"
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

    def gruppe_stufe_func(self, line: str):
        parts = line.split("Grundvergütung")[2].strip().split(" ")
        return (
            f"S{parts[1]}/{parts[3]}" if parts[0] == "S" else f"{parts[0]}/{parts[2]}"
        )


def process_abrechnungen(file_contents: list, year: str = "2024") -> bytes:
    """Process payroll (Abrechnungen) files and return Excel content as bytes."""
    pages = []
    for file_content in file_contents:
        print(f"Reading uploaded file...")
        text_pages = get_pages(file_content)
        for tpage in text_pages:
            page_obj = Page(tpage)
            if year not in page_obj.month_year:
                print(
                    f"Skipping page not for year {year} (RR={page_obj.is_rueckrechnung}): {page_obj}"
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
                        # Log change without exposing sensitive data
                        print(
                            f"Changed {table['name']} for employee, month {page.month}, RR={page.is_rueckrechnung}"
                        )
                data[page.month][page.name][table["name"]] = datapoint

    # Create Excel file in memory
    output = io.BytesIO()
    with ExcelWriter(output, engine="openpyxl", mode="w") as writer:
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
    
    output.seek(0)
    return output.getvalue()


def line_with(lines: list, text: str):
    """Find first line containing text."""
    return [line for line in lines if text in line][0]


def line_index_with(lines: list, text: str):
    """Find index of first line containing text."""
    return [index for index, line in enumerate(lines) if text in line][0]


def process_entry(
    data,
    nextLineRR,
    lineSplit: list,
    nextLineSplit: list,
    monat_header: str,
    gesamt_header: str,
    plus: bool,
    current_employee: str,
):
    """Process a single entry for AG Belastung."""
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


def process_ag_belastung(file_content: bytes, year: str = "2025", month: str = "AUGUST") -> bytes:
    """Process AG Belastung (Employer Burden) file and return Excel content as bytes."""
    HEADER_END = "Pers.Nr. Einheiten"
    FOOTER_START = "Lohnservice Wendel eG"
    
    pages = get_pages(file_content)
    
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
            print(f"--- BEGIN employee processing ---")
            RR_line_processed = process_entry(
                data, nextLineRR, lineSplit, nextLineSplit, MONATSBRUTTO, GESAMTBRUTTO, True, current_employee
            )
            continue
        if line.startswith("Zwischensummen"):
            current_employee_done = True
            print(f">data processed for employee")
            print(f"--- END employee processing ---\n")
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
                data, nextLineRR, lineSplit, nextLineSplit, SV_AG_MONAT, SV_AG_GESAMT, True, current_employee
            )
            continue
        if line.startswith("Erst. Entg. AU") or line.startswith("aus RR: Erst. Entg. AU"):
            RR_line_processed = process_entry(
                data, nextLineRR, lineSplit, nextLineSplit, U1_MONAT, U1_GESAMT, False, current_employee
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
                data, nextLineRR, lineSplit, nextLineSplit, U2_MONAT, U2_GESAMT, False, current_employee
            )
            continue

        raise OSError(f"Unable to process unknown line {line}")
    print("Finished reading")

    # Create Excel file in memory
    TITLE = "AG Belastung"
    output = io.BytesIO()
    with ExcelWriter(output, engine="openpyxl", mode="w") as writer:
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
    
    output.seek(0)
    return output.getvalue()


def find_index(data, element):
    """Find index of element in list."""
    for index, item in enumerate(data):
        if item == element:
            return index
    return -1


def format_float(number):
    """Format float number in European style."""
    integer_part, decimal_part = f"{number:.2f}".split(".")
    return f"{integer_part},{decimal_part}"


def process_aag_erstattungen(file_contents: list, year: str = "2024") -> bytes:
    """Process AAG Erstattungen (Reimbursements) files and return CSV content as bytes."""
    ROW_SUM = "Summe"
    erstattungen_u1 = {}
    erstattungen_u2 = {}

    for file_idx, file_content in enumerate(file_contents):
        text_pages = get_pages(file_content)
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
                print("ERROR finding type of page:")
                print(page)

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
            title = f"file_{file_idx + 1}"

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
    for name in erstattungen_u1.keys():
        erstattungen_u1[name][ROW_SUM] = sum(erstattungen_u1[name].values())
    for name in erstattungen_u2.keys():
        erstattungen_u2[name][ROW_SUM] = sum(erstattungen_u2[name].values())

    titles = [f"file_{i+1}" for i in range(len(file_contents))]
    print(f"\nProcessing {len(file_contents)} files")

    # Create CSV content in memory
    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")

    writer.writerow(["U1"])
    writer.writerow(["Name"] + titles + [ROW_SUM])
    for name in erstattungen_u1.keys():
        writer.writerow(
            [name]
            + [
                (
                    format_float(erstattungen_u1[name][x])
                    if x in erstattungen_u1[name]
                    else "0"
                )
                for x in titles
            ]
            + [format_float(erstattungen_u1[name][ROW_SUM])]
        )

    writer.writerow([])
    writer.writerow(["U2"])
    writer.writerow(["Name"] + titles + [ROW_SUM])
    for name in erstattungen_u2.keys():
        writer.writerow(
            [name]
            + [
                (
                    format_float(erstattungen_u2[name][x])
                    if x in erstattungen_u2[name]
                    else "0"
                )
                for x in titles
            ]
            + [format_float(erstattungen_u2[name][ROW_SUM])]
        )
    
    # Convert to bytes with UTF-8 BOM for CSV
    output.seek(0)
    csv_content = output.getvalue()
    return ('\ufeff' + csv_content).encode('utf-8')


def process_lohnjournal(file_content: bytes, year: str = "2024") -> bytes:
    """Process Lohnjournal (Payroll Journal) file and return Excel content as bytes."""
    HEADER_END = "Name E Kl"
    FOOTER_START = "Negative Werte sind"
    END_TEXT = "Summen: "
    
    pages = get_pages(file_content)

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
        i += 1
    print("Finished processing")

    # Create Excel file in memory
    TITLE = "Lohnjournal"
    output = io.BytesIO()
    with ExcelWriter(output, engine="openpyxl", mode="w") as writer:
        df = DataFrame.from_dict(data, orient="columns").T
        order = [STEUERBRUTTO, GESAMTBRUTTO, SV_AG]
        df = df[order]
        title_df = DataFrame([{"title": TITLE}])
        title_df.to_excel(writer, sheet_name=TITLE, index=False, header=False, startrow=0)
        df.to_excel(writer, sheet_name=TITLE, index=True, header=True, startrow=2)
        writer.sheets[TITLE].column_dimensions["A"].width = 30
        for column in ["B", "C", "D", "E", "F", "G", "H", "I"]:
            writer.sheets[TITLE].column_dimensions[column].width = 15
    
    output.seek(0)
    return output.getvalue()